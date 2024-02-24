import sqlite3

def generate_sql():
    # Table Team
    team_table_sql = """
    CREATE TABLE Team (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_name VARCHAR(255),
        date_registered DATE
    );
    """

    # Table Match
    match_table_sql = """
    CREATE TABLE Match (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_one_id INT,
        team_two_id INT,
        team_one_score INT,
        team_two_score INT,
        team_one_outs INT,
        team_two_outs INT,
        overs INT,
        winner_id INT,
        date_held DATE,
        FOREIGN KEY (team_one_id) REFERENCES Team(id),
        FOREIGN KEY (team_two_id) REFERENCES Team(id)
    );
    """

    # Table Player
    player_table_sql = """
    CREATE TABLE Player (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255),
        age INT,
        team_id INT,
        role INT,
        FOREIGN KEY (team_id) REFERENCES Team(id)
    );
    """

    # Table Over
    over_table_sql = """
    CREATE TABLE Over (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INT,
        match_id INT,
        team_id INT,
        player_id INT,
        FOREIGN KEY (match_id) REFERENCES Match(id),
        FOREIGN KEY (player_id) REFERENCES Player(id)
    );
    """

    # Table Extras
    extras_table_sql = """
    CREATE TABLE Extras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wides INT,
        no_balls INT,
        byes INT,
        leg_byes INT,
        match_id INT,
        team_id INT,
        FOREIGN KEY (match_id) REFERENCES Match(id),
        FOREIGN KEY (team_id) REFERENCES Team(id)
    );
    """


    # Table BattingStats
    batting_stats_table_sql = """
    CREATE TABLE BattingStats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INT,
        balls INT,
        sixes INT,
        fours INT,
        strike_rate FLOAT,
        dots INT,
        player_id INT,
        team_id INT,
        match_id INT,
        FOREIGN KEY (player_id) REFERENCES Player(id),
        FOREIGN KEY (match_id) REFERENCES Match(id)
    );
    """


    sql_code = (
        team_table_sql,
        match_table_sql,
        player_table_sql,
        over_table_sql,
        extras_table_sql,
        bowling_stats_table_sql,
        batting_stats_table_sql
    )

    return sql_code

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

sc = generate_sql()

try:
    for i in sc:
        cursor.execute(i)
    # Commit the changes
    conn.commit()
    print("Tables created successfully.")

except sqlite3.Error as e:
    print(f"Error: {e}")
    conn.rollback()

finally:
    # Close the connection
    conn.close()
