# qwikcut-stats-api
A RESTful API for QwikCut Sports Statistics Tracking

This backend database API is designed in Flask as a simple, lightweight Application Programming
Interface to be used by the QwikCut Stats Android app.

### Installation
First, your machine needs to run python. 
Make sure you have python installed on your machine. Type `python` to the command line. If it prints something like "Python 2.7.12 blah blah", you have python installed.

Second, you need to install some libraries to this local server.
I recommend using the tool called "pip." You can install the tool from this [link](https://pip.pypa.io/en/stable/installing/).
After you install "pip", open "requirements.txt" located under the root of this project. 
Install the library by typing "pip install EACH_LINE_IN_REQUIREMENTS.TXT." If everything is successfully loaded, you will see "Successfully installed" at the end of the install process.

There is a troubleshooting section in this document. Please refer to that section if you face any problem. If your problem is not found in the section, please ask for help or google. After you solve your issue, please add the issue and your solution to the troubleshooting section.

Third, you need to create `config.py` locally that stores DB connection setting.
Create a file called `config.py` and write these information in this folder. 
To connect to Azure database, you need to install extra library. Here is a [link](https://docs.microsoft.com/en-us/azure/sql-database/sql-database-connect-query-python#configure-development-environment) to the official support to connect to Azure database through Python. Please refer to this link to install necessary software. 

### Trouble shooting

1. import pyodbc doesn’t work (Mac)

error generates
ImportError: dlopen(/Users/koheiarai/anaconda/lib/python2.7/site-packages/pyodbc.so, 2): Library not loaded: /usr/local/opt/unixodbc/lib/libodbc.2.dylib
  Referenced from: /Users/koheiarai/anaconda/lib/python2.7/site-packages/pyodbc.so
  Reason: image not found

solution: install unixodbc
https://github.com/mkleehammer/pyodbc/issues/87

2. import pyodbc doesn’t work (Ubuntu)

This generates 

'#include <Python.h> No file or directory found
error: command `i686-linux-gnu-gcc` failed with exit status 1.

Install python-dev package by `sudo apt-get install python-dev`. If it succeeds, run `sudo pip install pyodbc==3.1.1`

3. FreeTSD is not found (Mac)

This trouble happens after your local server is up and running. When you try to login at http://127.0.0.1:5000/api/v1.0/, it prints error "'[unixODBC']'[Driver Manager']Can't open lib 'FreeTDS' : file not found". This is because your local server cannot establish valid connection with our Microsoft Azure setting.

Please follow this [answer on stackoverflow](http://stackoverflow.com/a/27239553) for Mac and for [this link especially **pyodbc** section](http://www.craigderington.me/design-an-api-with-flask-and-flask-restful-and-mysql/) for Ubuntu.

4. IP address is not set up for virtual box (Ubuntu)

This happens when setting up a server on virtual box hosting ubuntu. Not solved yet.

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


##### Usage Examples






