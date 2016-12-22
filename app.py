#! flask/bin/python

from flask import Flask, jsonify, abort, make_response, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import pypodbc

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    """ Simple text based authentication """
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


stat_fields = {
    'statid': field.Integer,
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
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()

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
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        self.reqparse.add_argument()
        super(StatAPI, self).__init__()

    def get(self, id):
        stat = [stat for stat in stats if stat['id'] == id]
        if len(stat) == 0:
            abort(404)
        return {'stat': marshal(stat[0], stat_fields)}

    def put(self, id):
        stat = [stat for stat in stats if stat['id'] == id]
        if len(stat) == 0:
            abort(404)
        stat = stat[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                stat[k] = v
        return {'stat': marshal(stat, stat_fields)}

    def delete(self, id):
        stat  [stat for stat in stats if stat['id'] == id]
        if len(stat) == 0:
            abort(404)
        stat.remove(stat[0])
        return {'result': True}


api.add_resource(StatListAPI, '/api/v1.0/lacrosse/stats', endpoint='stats')
api.add_resource(StatAPI, '/api/v1.0/lacrosse/stats/<int:statid>', endpoint='stat')

if __name__ == '__main__':
    app.run(debug=True)