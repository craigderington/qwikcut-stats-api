#! flask/bin/python

from flask import Flask, jsonify, abort, make_response, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import pyodbc

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    """ Simple text-based authentication """
    if username == 'qwikcutappstats':
        return 'thisispython'
    else:
        return None


@auth.error_handler
def unauthorized():
    """
    Return a 403 instead of a 401 to prevent broswsers from displaying
    the default auth dialog
    :param:
    :return: unauthorized message
    """
    return make_response(jsonify({'message': 'Unauthorized Access'}), 403)

stats = [
    {
        'statid': 4001,
        'playerid': 1234,
        'playernumber': 42,
        'goals': 2,
        'assists': 6,
        'saves': 0,
        'grounders': 2,
        'turnovers': 1,
        'forcedturnovers': 0,
        'penalties': 1
    },
    {
        'statid': 4002,
        'playerid': 1236,
        'playernumber': 86,
        'goals': 0,
        'assists': 12,
        'saves': 0,
        'grounders': 3,
        'turnovers': 0,
        'forcedturnovers': 0,
        'penalties': 2
    }
]

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
                                   help='The stat ID field is an auto-incrementing database field',
                                   location='json')
        self.reqparse.add_argument('playerid', type=int, required=False,
                                   help='The player ID is used to map the playner names to the team rosters.',
                                   location='json')
        self.reqparse.add_argument('playernumber', type=int, required=True,
                                   help='The player for which the game statistic is being recorded',
                                   location='json')
        self.reqparse.add_argument('goals', type=int, required=False,
                                   help='The number of goals scored.',
                                   location='json')
        self.reqparse.add_argument('shots', type=int, required=False,
                                   help='The number of shots taken.',
                                   location='json')
        self.reqparse.add_argument('assists', type=int, required=False,
                                   help='The number of assists.',
                                   location='json')
        self.reqparse.add_argument('saves', type=int, required=False,
                                   help='The number of saves.',
                                   location='json')
        self.reqparse.add_argument('grounders', type=int, required=False,
                                   help='The number of grounders.',
                                   location='json')
        self.reqparse.add_argument('turnovers', type=int, required=False,
                                   help='The number of turnovers.',
                                   location='json')
        self.reqparse.add_argument('forcedturnovers', type=int, required=False,
                                   help='The number of forced turnovers.',
                                   location='json')
        self.reqparse.add_argument('penalties', type=int, required=False,
                                   help='The number of penalties.',
                                   location='json')
        self.reqparse.add_argument('uri', type=str, required=False,
                                   help='The full URL path of the stat.')

        super(StatListAPI, self).__init__()

    def get(self):
        return {
            'stats': [marshal(stat, stat_fields) for stat in stats]
        }

    def post(self):
        args = self.reqparse.parse_args()
        stat = {
            'statid': args['statid'],
            'playerid': args['playerid'],
            'playernumber': args['playernumber'],
            'goals': args['goals'],
            'shots': args['shots'],
            'assists': args['assists'],
            'saves': args['saves'],
            'grounders': args['grounders'],
            'turnovers': args['turnovers'],
            'forcedturnovers': args['forcedturnovers'],
            'penalties': args['penalties']
        }
        stats.append(stat)
        return {'stat': marshal(stat, stat_fields)}, 201


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
                                   location='json')
        self.reqparse.add_argument('playerid', type=int, required=False,
                                   help='The player ID is used to map the playner names to the team rosters.',
                                   location='json')
        self.reqparse.add_argument('playernumber', type=int, required=True,
                                   help='The player for which the game statistic is being recorded',
                                   location='json')
        self.reqparse.add_argument('goals', type=int, required=False,
                                   help='The number of goals scored.',
                                   location='json')
        self.reqparse.add_argument('shots', type=int, required=False,
                                   help='The number of shots taken.',
                                   location='json')
        self.reqparse.add_argument('assists', type=int, required=False,
                                   help='The number of assists.',
                                   location='json')
        self.reqparse.add_argument('saves', type=int, required=False,
                                   help='The number of saves.',
                                   location='json')
        self.reqparse.add_argument('grounders', type=int, required=False,
                                   help='The number of grounders.',
                                   location='json')
        self.reqparse.add_argument('turnovers', type=int, required=False,
                                   help='The number of turnovers.',
                                   location='json')
        self.reqparse.add_argument('forcedturnovers', type=int, required=False,
                                   help='The number of forced turnovers.',
                                   location='json')
        self.reqparse.add_argument('penalties', type=int, required=False,
                                   help='The number of penalties.',
                                   location='json')
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
    app.run(debug=True)
