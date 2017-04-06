#! flask/bin/python

from flask import Flask, session, request, redirect, jsonify, abort, escape, make_response, url_for, \
    render_template, flash
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
import pyodbc
import json
from hashlib import sha384
import config


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
app.secret_key = config.SECRET_KEY


class ServerError(Exception):
    pass


class AzureSQLDatabase(object):
    connection = None
    cursor = None

    def __init__(self):
        self.connection = pyodbc.connect(config.CONN_STRING)
        self.cursor = self.connection.cursor()

    def query(self, query, params):
        return self.cursor.execute(query, params)

    def commit(self):
        return self.connection.commit()

    def __del__(self):
        self.connection.close()


@app.route('/api/v1.0/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    context = {
        "username_session": escape(session['username']).capitalize(),
        "userid": session['userid'],
        "teamname": session['teamname']
    }

    return render_template('index.html', context=context)


@app.route('/api/v1.0/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    error = None
    try:
        if request.method == 'POST':
            username_form = request.form['username']
            conn = AzureSQLDatabase()
            params = username_form
            sql = "select count(1) from users where username = ?;"
            cursor = conn.query(sql, params)

            if not cursor.fetchone()[0]:
                raise ServerError('Invalid Username!')

            password_form = request.form['password']
            params2 = password_form
            sql2 = "select password, userid, teamname from users where username = ?;"
            cursor2 = conn.query(sql2, params)

            for row in cursor2.fetchall():
                if sha384(password_form).hexdigest().upper() == row[0]:
                    session['username'] = request.form['username']
                    session['userid'] = row[1]
                    session['teamname'] = row[2]
                    return redirect(url_for('index'))

            raise ServerError('Invalid Password!')
    except ServerError as e:
        error = str(e)

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


@app.route('/api/v1.0/logout')
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('teamname', None)
    return redirect(url_for('index'))


@app.route('/api/v1.0/forgot')
def forgot_password():
    return render_template('forgot.html', username=None)

@auth.hash_password
def hash_password(password):
    return sha384(password).hexdigest().upper()

@auth.get_password
def get_password(username):
    conn = AzureSQLDatabase()
    sql = "select password from users where username = ?;"
    cursor = conn.query(sql, username)
    row = cursor.fetchone();
    
    if not row:
        return None
    else:
        return row.password
    
    """ Simple text-based authentication 
        Save these for later use in the future
    if username == 'qwikcutappstats':
        api_key = 'ebd7a876-c8ad-11e6-9d9d-cec0c932ce01'
        return api_key
    else:
        return None
    """


@auth.error_handler
def unauthorized():
    """
    Return a 403 instead of a 401 to prevent browsers from displaying
    the default auth dialog
    :param:
    :return: unauthorized message
    """
    return make_response(jsonify({'message': 'Unauthorized Access'}), 403)


stat_fields = {
    'id': fields.Integer,
    'statid': fields.Integer,
    'playerid': fields.Integer,
    'playernumber': fields.Integer,
    'goals': fields.Integer,
    'shots': fields.Integer,
    'assists': fields.Integer,
    'saves': fields.Integer,
    'grounders': fields.Integer,
    'turnovers': fields.Integer,
    'forcedturnovers': fields.Integer,
    'penalties': fields.Integer,
    'teamid': fields.Integer,
    'gameid': fields.Integer,
    'teamname': fields.String,
    'statdate': fields.DateTime,
    'userid': fields.Integer,
    'deviceid': fields.String,
    'uri': fields.Url('stat')
}


class StatListAPI(Resource):
    """
    API Resource for listing all player stats from the database.
    Provides the endpoint for creating new stats
    :param: none
    :type a json object
    :return json stats list for all players
    """
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=int, required=False,
                                   help='The API URL\'s ID of the stat.')
        self.reqparse.add_argument('statid', type=int, required=False,
                                   help='The stat ID field is an auto-incrementing database field')
        self.reqparse.add_argument('playerid', type=int, required=False,
                                   help='The player ID is used to map the player names to the team rosters.')
        self.reqparse.add_argument('playernumber', type=int, required=False,
                                   help='The player for which the game statistic is being recorded.')
        self.reqparse.add_argument('goals', type=int, required=False,
                                   help='The number of goals scored.')
        self.reqparse.add_argument('shots', type=int, required=False,
                                   help='The number of shots taken.')
        self.reqparse.add_argument('assists', type=int, required=False,
                                   help='The number of assists.')
        self.reqparse.add_argument('saves', type=int, required=False,
                                   help='The number of saves.',
                                   location='form')
        self.reqparse.add_argument('grounders', type=int, required=False,
                                   help='The number of grounders.')
        self.reqparse.add_argument('turnovers', type=int, required=False,
                                   help='The number of turnovers.')
        self.reqparse.add_argument('forcedturnovers', type=int, required=False,
                                   help='The number of forced turnovers.')
        self.reqparse.add_argument('penalties', type=int, required=False,
                                   help='The number of penalties.',
                                   location='form')
        self.reqparse.add_argument('teamid', type=int, required=False,
                                   help='The team ID of the player.')
        self.reqparse.add_argument('gameid', type=int, required=False,
                                   help='Game ID for which this stat is being recorded.')
        self.reqparse.add_argument('teamname', type=str, required=False,
                                   help='The team name of the player stat')
        self.reqparse.add_argument('statdate', type=str,
                                   required=False, help='The stat date.')
        self.reqparse.add_argument('userid', type=int, required=False,
                                   help='The user ID of the logged in user.')
        self.reqparse.add_argument('deviceid', type=str, required=False,
                                   help='The unique device ID')
        self.reqparse.add_argument('uri', type=str, required=False,
                                   help='The full URL path of the stat.')

        super(StatListAPI, self).__init__()

    def get(self):
        try:
            sql = u"select statid, statid as id, playerid, playernumber, goals, shots, assists, " \
                  u"saves, grounders, turnovers, forcedturnovers, penalties, gameid, teamid, teamname, " \
                  u"statdate, userid from lacrosse_stats WHERE statdate > ?"

            conn = AzureSQLDatabase()
            params = '12-1-2016'
            cursor = conn.query(sql, params)
            columns = [column[0] for column in cursor.description]
            stats = []
            for row in cursor.fetchall():
                stats.append(dict(zip(columns, row)))

            return {
                'stats': marshal(stats, stat_fields)
            }

        except Exception as e:
            return {'error': str(e)}

    def post(self):
        try:
            args = self.reqparse.parse_args()
            data = request.get_json()
            stat = []

            stat = {
                'statid': data['statid'],
                'playerid': data['playerid'],
                'playernumber': data['playernumber'],
                'goals': data['goals'],
                'shots': data['shots'],
                'assists': data['assists'],
                'saves': data['saves'],
                'grounders': data['grounders'],
                'turnovers': data['turnovers'],
                'forcedturnovers': data['forcedturnovers'],
                'penalties': data['penalties'],
                'teamid': data['teamid'],
                'gameid': data['gameid'],
                'teamname': data['teamname'],
                'statdate': data['statdate'],
                'userid': data['userid'],
                'deviceid': data['deviceid']
            }

            conn = AzureSQLDatabase()
            conn.query("insert into lacrosse_stats(playerid, playernumber, goals, shots, assists, saves, grounders, \
                        turnovers, forcedturnovers, penalties, teamid, gameid, teamname, statdate, userid, deviceid) \
                        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       [stat['playerid'], stat['playernumber'], stat['goals'], stat['shots'], stat['assists'], stat['saves'], stat['grounders'], stat['turnovers'], stat['forcedturnovers'], stat['penalties'], stat['teamid'], stat['gameid'], stat['teamname'], stat['statdate'], stat['userid'], stat['deviceid']])

            conn.commit()

            return {
                'stat': stat
            }, 201

        except Exception as e:
            return {'error': str(e)}


class StatAPI(Resource):
    """
    API Resource for retrieving, modifying, updating and deleting a single
    player stat, by ID.
    :param: statid
    :return: player stat records by ID.
    """
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=int, required=False,
                                   help='The API URL\'s ID of the stat.')
        self.reqparse.add_argument('statid', type=int, required=False,
                                   help='The stat ID field is an auto-incrementing database field',
                                   location='args')
        self.reqparse.add_argument('playerid', type=int, required=False,
                                   help='The player ID is used to map the player names to the team rosters.',
                                   location='args')
        self.reqparse.add_argument('playernumber', type=int, required=True,
                                   help='The player for which the game statistic is being recorded',
                                   location='args')
        self.reqparse.add_argument('goals', type=int, required=False,
                                   help='The number of goals scored.',
                                   location='args')
        self.reqparse.add_argument('shots', type=int, required=False,
                                   help='The number of shots taken.',
                                   location='args')
        self.reqparse.add_argument('assists', type=int, required=False,
                                   help='The number of assists.',
                                   location='args')
        self.reqparse.add_argument('saves', type=int, required=False,
                                   help='The number of saves.',
                                   location='args')
        self.reqparse.add_argument('grounders', type=int, required=False,
                                   help='The number of grounders.',
                                   location='args')
        self.reqparse.add_argument('turnovers', type=int, required=False,
                                   help='The number of turnovers.',
                                   location='args')
        self.reqparse.add_argument('forcedturnovers', type=int, required=False,
                                   help='The number of forced turnovers.',
                                   location='args')
        self.reqparse.add_argument('penalties', type=int, required=False,
                                   help='The number of penalties.',
                                   location='args')
        self.reqparse.add_argument('teamid', type=int, required=False,
                                   help='The QC+ team ID of the player.')
        self.reqparse.add_argument('gameid', type=int, required=False,
                                   help='The QC+ game ID from the games table.')
        self.reqparse.add_argument('teamname', type=str, required=True,
                                   help='The player\'s team name.')
        self.reqparse.add_argument('statdate', type=str, required=True,
                                   help='The date time stamp of the statistic.')
        self.reqparse.add_argument('uri', type='str', required=False,
                                   help='The full URL path to the requested resource')
        super(StatAPI, self).__init__()

    def get(self, id):
        try:
            conn = AzureSQLDatabase()
            params = id
            sql = u"select statid, statid as id, playerid, playernumber, goals, shots, assists, saves, grounders, turnovers, " \
                  u"forcedturnovers, penalties, teamid, gameid, teamname, statdate, userid from lacrosse_stats where statid = ?"

            cursor = conn.query(sql, params)
            columns = [column[0] for column in cursor.description]
            stat = []
            for row in cursor.fetchall():
                stat.append(dict(zip(columns, row)))

            return {
                'stat': marshal(stat, stat_fields)
            }, 200

        except Exception as e:
            return {'error': str(e)}

    def put(self, id):
        try:
            conn = AzureSQLDatabase()
            data = request.get_json()
            params = (data['playerid'], data['playernumber'], data['goals'], data['shots'], data['assists'], data['saves'], data['grounders'], data['turnovers'], data['forcedturnovers'], data['penalties'], data['teamid'], data['gameid'], data['teamname'], data['statdate'], id)
            conn.query("update lacrosse_stats set playerid = ?, playernumber = ?, goals = ?, shots = ?, assists = ?, \
                        saves = ?, grounders = ?, turnovers = ?, forcedturnovers = ?, penalties = ?, teamid = ?, \
                        gameid = ?, teamname = ?, statdate = ? where statid = ?", params)

            conn.commit()

            return {
                'stat': data
            }, 204

        except Exception as e:
            return {'error': str(e)}

    def delete(self, id):
        try:
            conn = AzureSQLDatabase()
            params = id
            sql = u"delete from lacrosse_stats where statid = ?"
            cursor = conn.query(sql, params)
            conn.commit()

            return {
                'result': True
            }, 204

        except Exception as e:
            return {'error': str(e)}


# register the API resources and define endpoints
api.add_resource(StatListAPI, '/api/v1.0/lacrosse/stats', endpoint='stats')
api.add_resource(StatAPI, '/api/v1.0/lacrosse/stats/<int:id>', endpoint='stat')

if __name__ == '__main__':
    app.run(
        debug=config.DEBUG,
        port=config.PORT
    )
