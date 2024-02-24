import os
import sqlite3 as sq
import sys

sys.path.append('../')

current_dir = os.path.dirname(os.path.realpath(__file__))
db_file_path = os.path.join(current_dir, '..', 'your_database.db')

conn = sq.connect(db_file_path)
cursor = conn.cursor()
print("Roles: Batsman, Bowler, AR")
print()
rol = input('Enter Role: ').upper()

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
        p.role = ? AND
        p.team_id = t.id
"""

mt = conn.execute(query, (rol,)).fetchall()
print('Name                  Age        Role     Team')
print('==================================================')
i=1
for p in mt:
    print(i,': ',p[0].ljust(16), str(p[1]).ljust(10), p[2].ljust(8),p[3])
    i=i+1
