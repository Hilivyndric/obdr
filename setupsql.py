import sqlite3

with open('setup.SQL', 'r') as sql_file:
    sql_script = sql_file.read()

db = sqlite3.connect('obdrocheno.db')
cursor = db.cursor()
cursor.executescript(sql_script)
db.commit()
db.close()
cursor.close()