#! flask/bin/python

from flask import Flask, request, jsonify, abort, make_response, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import pyodbc
import json
import config


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


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


@auth.get_password
def get_password_and_key(username):
    """ Simple text-based authentication """
    if username == 'qwikcutappstats':
        api_key = 'ebd7a876-c8ad-11e6-9d9d-cec0c932ce01'
        return api_key
    else:
        return None


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
    'uri': fields.Url('stat')
}


class StatListAPI(Resource):
    """
    API Resource for listing all player stats from the database.
    Provides the endpoint for creating new stats
    :param:
    :return json stats list for all players
    """
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('statid', type=int, required=False,
                                   help='The stat ID field is an auto-incrementing database field')
        self.reqparse.add_argument('playerid', type=int, required=False,
                                   help='The player ID is used to map the player names to the team rosters.')
        self.reqparse.add_argument('playernumber', type=int, required=False,
                                   help='The player for which the game statistic is being recorded.')
        self.reqparse.add_argument('goals', type=int, required=False,
                                   help='The number of goals scored.')
        self.reqparse.add_argument('shots', type=int, required=False,
                                   help='The number of shots taken.',
                                   location='form')
        self.reqparse.add_argument('assists', type=int, required=False,
                                   help='The number of assists.',
                                   location='form')
        self.reqparse.add_argument('saves', type=int, required=False,
                                   help='The number of saves.',
                                   location='form')
        self.reqparse.add_argument('grounders', type=int, required=False,
                                   help='The number of grounders.',
                                   location='form')
        self.reqparse.add_argument('turnovers', type=int, required=False,
                                   help='The number of turnovers.',
                                   location='form')
        self.reqparse.add_argument('forcedturnovers', type=int, required=False,
                                   help='The number of forced turnovers.',
                                   location='form')
        self.reqparse.add_argument('penalties', type=int, required=False,
                                   help='The number of penalties.',
                                   location='form')
        self.reqparse.add_argument('teamid', type=int, required=False,
                                   help='The team ID of the player.',
                                   location='form')
        self.reqparse.add_argument('gameid', type=int, required=False,
                                   help='Game ID for which this stat is being recorded.',
                                   location='form')
        self.reqparse.add_argument('teamname', type=str, required=False,
                                   help='The team name of the player stat',
                                   location='form')
        self.reqparse.add_argument('statdate', type=str, required=False,
                                   help='The stat date.',
                                   location='form')
        self.reqparse.add_argument('uri', type=str, required=False,
                                   help='The full URL path of the stat.')

        super(StatListAPI, self).__init__()

    def get(self):
        sql = u"select statid, playerid, playernumber, goals, shots, assists, saves, grounders, turnovers, forcedturnovers, \
                penalties, gameid, teamid, teamname, statdate from lacrosse_stats WHERE statdate > ?"
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

    def post(self):
        args = self.reqparse.parse_args()
        data = request.get_json()
        stat = []

        for key, value in data.items():
            stat.append(dict(zip(key, value)))

        """
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
            'statdate': data['statdate']
        }

        conn = AzureSQLDatabase()
        conn.query("insert into lacrosse_stats(playerid, playernumber, goals, shots, assists, saves, grounders, \
                    turnovers, forcedturnovers, penalties, teamid, gameid, teamname, statdate) \
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   [stat['playerid'], stat['playernumber'], stat['goals'], stat['shots'], 23, 0, 0, 0, 0, 1, 321, 1323, 'Wesley Chappel', '12-23-2016 13:23:32'])
        conn.commit()

        return {
            'stat': marshal(stat, stat_fields)
        }, 201

        """

        return {'stat': stat}, 200

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
        super(StatAPI, self).__init__()

    def get(self, id):
        stat = [stat for stat in stats if stat['statid'] == id]
        if len(stat) == 0:
            abort(404)
        return {'stat': marshal(stat[0], stat_fields)}

    def put(self, id):
        stat = [stat for stat in stats if stat['statid'] == id]
        if len(stat) == 0:
            abort(404)
        stat = stat[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                stat[k] = v
        return {'stat': marshal(stat, stat_fields)}

    def delete(self, id):
        stat = [stat for stat in stats if stat['statid'] == id]
        if len(stat) == 0:
            abort(404)
        stat.remove(stat[0])
        return {'result': True}

# register the API resources and define endpoints
api.add_resource(StatListAPI, '/api/v1.0/lacrosse/stats', endpoint='stats')
api.add_resource(StatAPI, '/api/v1.0/lacrosse/stats/<int:statid>', endpoint='stat')

if __name__ == '__main__':
    app.run(
        debug=config.DEBUG,
        port=config.PORT
    )
