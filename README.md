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
* GET ['/api/version/login']
* POST ['/api/version/login']
* GET ['/api/version/index']
* GET ['api/version/logout']

where sport is the name of the sport in which the enduser is recording game statistics.

##### Lacrosse Fields

```
stat_fields = {
    'id': fields.Integer, // field for marshalling <int:statid>
    'statid': fields.Integer,  // auto-incrementing PK field from Azure DB
    'userid': fields.Integer, // set to unique user id
    'playerid': fields.Integer, // set to 0 for default
    'playernumber': fields.Integer,
    'goals': fields.Integer,
    'shots': fields.Integer,
    'assists': fields.Integer,
    'saves': fields.Integer,
    'grounders': fields.Integer,
    'turnovers': fields.Integer,
    'forcedturnovers': fields.Integer,
    'penalties': fields.Integer,
    'teamid': fields.Integer, // set to 0 for default
    'gameid': fields.Integer, // set to 0 for default
    'teamname': fields.String,
    'statdate': fields.DateTime,
    'deviceid': fields.String,
    'uri': fields.Url('stat') // auto-generated URI field
}
```

##### JSON Data format for POST:  Example

```
{
    "id": 0,
    "statid": 0,
    "playerid": 2434,
    "playernumber": 36,
    "goals": 2,
    "shots": 6,
    "assists": 0,
    "saves": 0,
    "grounders": 3,
    "turnovers": 0,
    "forcedturnovers": 0,
    "penalties": 2,
    "teamid": 1190,
    "gameid": 1634,
    "teamname": "Clemson Tigers",
    "statdate": "2017-01-10 09:30:45",
    "userid": 7654,
    "deviceid": "4aec0906-d9b9-47d6-842d-bcd998e665d8"
}
```

##### Lacrosse Endpoints

* GET ['/api/v1.0/lacrosse/stats']
* POST ['/api/v1.0/lacrosse/stats']
* DELETE ['/api/v1.0/lacrosse/stats/<int:statid>']
* GET ['/api/v1.0/lacrosse/stats/<int:statid>']
* PATCH ['/api/v1.0/lacrosse/stats/<int:statid>]'
* PUT ['/api/v1.0/lacrosse/stats/<int:statid>']


##### API/App - Authentication Endpoints

* GET ['/api/v1.0/login']
* POST ['/api/v1.0/login']
* GET ['/api/v1.0/index']
* GET ['/api/v1.0/logout']

Example:  POST to http://.../api/v1.0/login

```
form_vars = {
   "username": username, 
   "password": password
}
```

Upon successful login, returns username, user ID and team name

##### Usage Examples

GET:

curl -i -H --user username:password "Accept: application/json" -H "Content-Type: application/json" -X GET http://server_ip/api/v1.0/lacrosse/stats

POST:

curl -i -H --user username:password "Accept: application/json" -H "Content-Type: application/json" -X POST -d 'payload={"playerid": 0, "playernumber": "42", "goals": 2, "remaining fields": 23}' http://server_ip/api/v1.0/lacrosse/stats

GET <int:statid>

curl -i -H --user username:password "Accept: application/json" -H "Content-Type: application/json" -X GET http://server_ip/api/v1.0/lacrosse/stats/26









