import os
import sqlite3 as sq
import sys
sys.path.append('../')
import sampleData as data
db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'your_database.db'))


conn = sq.connect(db_file_path)
cursor = conn.cursor()

name = input('Enter team name: ')

query = """
    SELECT
        p.name,
        p.age,
        p.role,
        t.team_name
    FROM
        Player as p
    INNER JOIN
        Team as t
    WHERE
        p.team_id = t.id AND
        t.team_name = ?
    """
try:

    mt = conn.execute(query,(name,)).fetchall()

    print('Name             Age       Role            Team')
    print('=========================================================')
    for p in mt:
        print(p[0].ljust(16),str(p[1]).ljust(9),p[2].ljust(15),p[3])


    conn.close()
except:
    print('Team not found')
