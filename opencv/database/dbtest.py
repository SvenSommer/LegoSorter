#!/usr/bin/python
import pymysql

db = pymysql.connect(host="localhost",    # your host, usually localhost
                     user="WebDBUser",         # your username
                     passwd="qF2J%9a84zU",  # your password
                     db="LegoSorterDB")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

sql = """INSERT INTO `LegoSorterDB`.`Partimages`
(`run_id`,
`path`,
`size_kb`,
`created`,
`imported`,
`deleted`)
VALUES
(<{run_id: }>,
<{path: }>,
<{size_kb: }>,
<{created: }>,
<{imported: }>,
<{deleted: }>);"""

# Use all the SQL you like
cur.execute("SELECT * FROM Sets")

# print all the first cell of all the rows
for row in cur.fetchall():
    print(row[2])

db.close()