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





