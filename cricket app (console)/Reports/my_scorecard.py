import os
import sqlite3 as sq
db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'your_database.db'))

conn = sq.connect(db_file_path)
cursor = conn.cursor()

try:
    matches_query = """
                SELECT
                    m.id AS match_id,
                    t1.team_name AS team_one_name,
                    t2.team_name AS team_two_name
                FROM
                    Match AS m
                INNER JOIN
                    Team AS t1 ON t1.id = m.team_one_id
                INNER JOIN
                    Team AS t2 ON t2.id = m.team_two_id
            """
    matches_data = conn.execute(matches_query).fetchall()
    print("\nAvailable Matches:")
    for match in matches_data:
        match_id, team_one_name, team_two_name = match
        print(f"Match #{match_id}: {team_one_name} vs {team_two_name}")
except sq.Error as e:
    print(f"Error fetching matches: {e}")


conn.close()
class Scorecard:
    def __init__(self, db_file_path,match_id):
        self._db_file_path = db_file_path
        self._conn = sq.connect(self._db_file_path)
        self._cursor = self._conn.cursor()
        self.match_id = match_id

    @property
    def db_file_path(self):
        return self._db_file_path

    @property
    def conn(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor


    def execute_query(self, query, params=None):
        if params:
            return self.conn.execute(query, params).fetchall()
        else:
            return self.conn.execute(query).fetchall()

    def display_scorecard(self, team_name, team_data, team_extras, total_extras, team_outs, opponent_name, opponent_bowling,balls_played):
        print(f'\n-----------------------------------{team_name} innings---------------------------------------------------------\n')
        print("Batsman        Score          Balls         Sixes         Fours         Dots        SR")
        for i, b in enumerate(team_data, start=1):
            print(f"{i}: {str(b[0]).ljust(14)} {str(b[1]).ljust(14)} {str(b[2]).ljust(13)} {str(b[3]).ljust(13)} {str(b[4]).ljust(13)} {str(b[5]).ljust(11)} {str(b[6]).ljust(20)}")
        ov = balls_played//6
        bal = balls_played%6
        for e in team_extras:
            print(f"\nExtras: {total_extras}   {e[0]}w, {e[1]}n, {e[2]}lb, {e[3]}b")
        print(f'Score:{sum(e[1] for e in team_data) +total_extras}  wickets:{team_outs}  overs:{ov}.{bal}')
        
        print()
        
        print(f'{opponent_name} Bowling:')
        print('\nover    Bowler            Score')
        for i, player in enumerate(opponent_bowling, start=1):
            print(f"{i}      {player[0].ljust(17)} {player[1]}")

    def display_winner(self, winner_id, team_one_name, team_two_name, score1, score2, team_one_outs, team_two_outs,team_one_balls,team_two_balls,overs):
        print("\n" + "-" * 110)
        #batting_first = self.execute_query(f"SELECT batting_first FROM Team WHERE id = {winner_id}")[0][0]

        
        #winner_name = self.execute_query(f"SELECT team_name FROM Team WHERE id = {winner_id}")[0][0]
        if score1>score2:

            print(f"{team_one_name} won by {score1 - score2} runs")
        elif score2>score1:
                print(f"{team_two_name} won by {10 - team_two_outs} wickets with {6*overs-team_two_balls} balls remaining")
       
        else:
            print("\nThe match ended in a draw!")

    def close_connection(self):
        self.conn.close()

    def process_match(self):
        # Fetch match information
        match_query = """
            SELECT
                m.id AS match_id,
                m.team_one_id,
                t1.team_name AS team_one_name,
                m.team_two_id,
                t2.team_name AS team_two_name,
                m.team_one_outs,
                m.team_two_outs,
                m.winner_id,
                m.team_one_balls,
                m.team_two_balls,
                m.overs
            FROM
                Match AS m
            INNER JOIN
                Team AS t1 ON t1.id = m.team_one_id
            INNER JOIN
                Team AS t2 ON t2.id = m.team_two_id
            WHERE
                m.id = ?
        """

        match_data = self.execute_query(match_query,(self.match_id,))

        for row in match_data:
            match_id, team_one_id, team_one_name, team_two_id, team_two_name, team_one_outs, team_two_outs, winner_id,team_one_balls,team_two_balls,overs = row

            # Team One Scorecard
            team_one_query = """
                SELECT
                    p.name,
                    b.score,
                    b.balls,
                    b.sixes,
                    b.fours,
                    b.dots,
                    b.strike_rate
                FROM 
                    BattingStats AS b
                INNER JOIN 
                    Player AS p ON b.player_id = p.id
                WHERE
                    b.team_id = ?
                    AND b.match_id = ?
            """

            team_one_data = self.execute_query(team_one_query, (team_one_id,self.match_id))
            team_one_extras = self.execute_query("SELECT wides, no_balls, leg_byes, byes FROM Extras WHERE team_id = ? AND match_id = ?", (team_one_id, self.match_id))
            total_extras1 = sum(sum(e) for e in team_one_extras)

            # Team Two Bowling
            bowling_query = """
                SELECT
                    p.name,
                    o.score,
                    o.match_id,
                    o.team_id,
                    o.player_id
                FROM
                    Over as o
                INNER JOIN 
                    Player AS p ON o.player_id = p.id
                WHERE o.match_id = ? AND o.team_id = ?
            """
            team_two_bowling = self.execute_query(bowling_query, (match_id, team_two_id))

            self.display_scorecard(team_one_name, team_one_data, team_one_extras, total_extras1, team_one_outs, team_two_name, team_two_bowling,team_one_balls)

            
            team_two_query = """
                SELECT
                    p.name,
                    b.score,
                    b.balls,
                    b.sixes,
                    b.fours,
                    b.dots,
                    b.strike_rate
                FROM 
                    BattingStats AS b
                INNER JOIN 
                    Player AS p ON b.player_id = p.id
                WHERE
                    b.team_id = ? AND
                    b.match_id = ?
            """

            team_two_data = self.execute_query(team_two_query, (team_two_id,self.match_id))
            team_two_extras = self.execute_query("SELECT wides, no_balls, leg_byes, byes FROM Extras WHERE team_id = ? AND match_id = ?", (team_two_id, match_id))
            total_extras2 = sum(sum(e) for e in team_two_extras)

            # Team One Bowling
            team_one_bowling = self.execute_query(bowling_query, (match_id, team_one_id))

            self.display_scorecard(team_two_name, team_two_data, team_two_extras, total_extras2, team_two_outs, team_one_name, team_one_bowling,team_two_balls)

            self.display_winner(winner_id, team_one_name, team_two_name, sum(e[1] for e in team_one_data)+total_extras1, sum(e[1] for e in team_two_data)+total_extras2, team_one_outs, team_two_outs,team_one_balls,team_two_balls,overs)

        # Close the connection
        self.close_connection()

if __name__ == "__main__":
    db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'your_database.db'))
    
    try:
        match_id = int(input('Enter match id: '))
        cricket_match = Scorecard(db_file_path, match_id)
        cricket_match.process_match()
    except ValueError:
        print("Invalid match id. Please enter a valid integer.")


