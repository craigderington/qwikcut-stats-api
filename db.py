import pyodbc

# define the connection
connection = pyodbc.connect('DRIVER={FreeTDS};SERVER=i1l7fad5wi.database.windows.net;PORT=1433;DATABASE=qwikcutapp;UID=<user>;PWD=<pass>;TDS_Version=7.0')

# set up our db cursor
cursor = connection.cursor()
SQLCommand = ("SELECT confid, stateid, confname, conftype "
              "FROM dbo.conferences "
              "ORDER BY confid ASC")

# execute the sql statement
cursor.execute(SQLCommand)

# put the results into a variable
results = cursor.fetchone()

# output the results
while results:
    print("Conference " + str(results[0]) + " in state: " + str(results[1]) \
          + " is named: " + results[2] + " with type " + results[3] + ".")
    results = cursor.fetchone()

# close the connection
connection.close()
