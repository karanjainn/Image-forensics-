# import sqlite3
from cs50 import SQL
from flask import render_template

#Create/connect to SQLite Database
db = SQL('sqlite:///data.db')

# db.execute("CREATE TABLE image_metadata2(abc integer,def integer)")
# db.execute("INSERT INTO image_metadata2(abc,def) values(1,2)")
rows = db.execute("SELECT * FROM image_metadata")

# connection.commit()
#Close connection
# connection.close()
print(rows)

# render_template("test.html",data = rows)
