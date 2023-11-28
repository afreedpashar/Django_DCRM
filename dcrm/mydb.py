import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Root@123',

)

#prepare a cursor objects
cursorObject = dataBase.cursor()

#create a data base
cursorObject.execute("CREATE DATABASE my_database")

print("ALL done!")