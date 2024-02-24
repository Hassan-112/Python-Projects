import os
import sqlite3 as sq
import sys
sys.path.append('../')

current_dir = os.path.dirname(os.path.realpath(__file__))
db_file_path = os.path.join(current_dir, '..', 'your_database.db')



conn = sq.connect(db_file_path)
cursor = conn.cursor()

query = """
    SELECT
        t.team_name,
        t.date_registered
    FROM
        Team as t
"""

mt = conn.execute(query).fetchall()
print('Team Name                 Date of Registration')
print('==============================================')
for p in mt:
    print(p[0].ljust(25),p[1])
