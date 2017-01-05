# qwikcut-stats-api
A RESTful API for QwikCut Sports Statistics Tracking

This backend database API is designed in Flask as a simple, lightweight Application Programming
Interface to be used by the QwikCut Stats Android app.

##### Resources

* StatListAPI
* StatAPI


##### Endpoints

* GET ['/api/version/sport/stats']
* POST ['/api/version/sport/stats']
* DELETE ['/api/version/sport/stats/<int:statid>']
* GET ['/api/version/sport/stats/<int:statid>']
* PATCH ['/api/version/sport/stats/<int:statid>]'
* PUT ['/api/version/sport/stats/<int:statid>']

where sport is the name of the sport in which the enduser is recording game statistics.

##### Lacrosse Fields

stat_fields = {
    'id': fields.Integer, // field for marshalling <int:statid>
    'statid': fields.Integer,  // auto-incrementing PK field from Azure DB 
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
    'uri': fields.Url('stat') // auto-generated URI field
}

##### Lacrosse Endpoints

* GET ['/api/v1.0/lacrosse/stats']
* POST ['/api/v1.0/lacrosse/stats']
* DELETE ['/api/v1.0/lacrosse/stats/<int:statid>']
* GET ['/api/v1.0/lacrosse/stats/<int:statid>']
* PATCH ['/api/v1.0/lacrosse/stats/<int:statid>]'
* PUT ['/api/v1.0/lacrosse/stats/<int:statid>']

##### Usage Examples

GET:

curl -i -H --user username:password "Accept: application/json" -H "Content-Type: application/json" -X GET http://<IP>/api/v1.0/lacrosse/stats

POST:

curl -i -H --user username:password "Accept: application/json" -H "Content-Type: application/json" -X POST -d 'payload={"stat": {"playerid": 0, "playernumber": "42", "goals": 2}}' http://<IP>/api/v1.0/lacrosse/stats/<int:statid>









