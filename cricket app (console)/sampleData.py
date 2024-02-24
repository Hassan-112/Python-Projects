import sqlite3 as sq

conn = sq.connect('your_database.db')
cursor = conn.cursor()
def close_database():
    conn.close()
class add_player:
    def __init__(self,player_name,player_team_id,age,role):
        

        self.__player_name = player_name
        self.__player_team_id = player_team_id
        self.__age = age
        if role == "AR" or role == "BOWLER" or role == "BATSMAN":
            self.__role = role
        else:

            raise Exception("Invalid role")

    def add_to_database(self):

        try:
                
              
            query = """
            INSERT INTO Player (name, age, team_id, role) VALUES
            (?,?,?,?);
            """
            values = (
                self.__player_name,
                self.__age,
                self.__player_team_id,
                self.__role
                )
                
            cursor.execute(query,values)
            conn.commit()
            print('Player added successfully!')

        except sq.Error as e:
            print(f"Error adding data to the database: {e}")
            
    def close_database(self):
        conn.close()
class register_team:

    def __init__(self,team_name,date_registered):
        self.team_name = team_name
        self.date_registered = date_registered
    def add_to_database(self):

        try:
                
            query = """
            INSERT INTO team (team_name, date_registered) VALUES
            (?,?);
            """
            values = (

                self.team_name,
                self.date_registered
                )
                    
            cursor.execute(query,values)
            conn.commit()
            print('Team registered successfully!')

        except sq.Error as e:
            print(f"Error adding data to the database: {e}")

    def close_database(self):
        conn.close()

class cricket:

    class batting_stats:
        def __init__(self,player_id,match_id,score,balls,sixes,fours,dots,team_id):
            self.dots = dots
            self.score = score
            self.balls = balls
            self.sixes = sixes
            self.fours = fours
            self.player_id = player_id
            self.match_id = match_id
            self.team_id = team_id

            if balls>0:
                self.strike_rate = self.score/self.balls*100
                self.strike_rate = f'{self.strike_rate:.2f}'
            else:
                self.strike_rate = 0.0
        def add_to_database(self):
            try:

                query = """
                INSERT INTO BattingStats (score,balls,sixes,fours,strike_rate,dots,player_id,match_id,team_id) VALUES
                (?,?,?,?,?,?,?,?,?);
                """
                values = (
                    self.score,
                    self.balls,
                    self.sixes,
                    self.fours,
                    self.strike_rate,
                    self.dots,
                    self.player_id,
                    self.match_id,
                    self.team_id
                )

                cursor.execute(query, values)
                conn.commit()
                print('Player stats added successfully!')

            except sq.Error as e:
                print(f"Error adding data to the database: {e}")


    class match:

        def __init__(self,overs,team_one_id,team_two_id,team_one_outs,team_two_outs,date_held,balls1,balls2):
            self.team_one_outs = team_one_outs
            self.team_two_outs = team_two_outs
            self.team_one_id = team_one_id
            self.team_two_id = team_two_id
            self.date_held = date_held
            self.overs = overs
            self.balls1 = balls1
            self.balls2 = balls2

        def add_to_database(self):

            try:
                query = """
                INSERT INTO Match (team_one_id, team_two_id,overs,team_one_outs,team_two_outs,
                date_held,team_one_balls,team_two_balls)
                VALUES (?,?,?,?,?,?,?,?);
                """
                values = (

                    self.team_one_id,
                    self.team_two_id,
                    self.overs,
              
                    self.team_one_outs,
                    self.team_two_outs,
                    self.date_held,
                    self.balls1,
                    self.balls2
                    )
                cursor.execute(query,values)
                conn.commit()
                print('Match data added successfully!')

            except sq.Error as e:
                print(f"Error adding data to the database: {e}")


    class over:

        def __init__(self,player_id,match_id,score,team_id,wickets):
            self.wickets = wickets
            self.player_id = player_id
            self.score = score
            self.match_id = match_id
            self.team_id = team_id

        def add_to_database(self):
            try:
                
                query = """
                INSERT INTO Over (player_id,match_id,score,team_id,wickets) VALUES (?,?,?,?,?);
                """
                values = (
                    self.player_id,
                    self.match_id,
                    self.score,
                    self.team_id,
                    self.wickets
                    )
                cursor.execute(query,values)
                conn.commit()
                print('over data added successfully!')

            except sq.Error as e:
                print(f"Error adding data to the database: {e}")
    class extras:
        def __init__(self,match_id,team_id,wides,no,lb,b):

            self.team_id = team_id
            self.match_id= match_id
            self.wides= wides
            self.no = no
            self.lb = lb
            self.b = b
        def add_to_database(self):
            try:
                query = """
                INSERT INTO Extras (wides,no_balls,byes,leg_byes,match_id,team_id) VALUES (?,?,?,?,?,?);
                """
                values = (
                    self.wides,
                    self.no,
                    self.b,
                    self.lb,
                    self.match_id,
                    self.team_id
                    )
                cursor.execute(query,values)
                conn.commit()
                print('extras added successfully!')

            except sq.Error as e:
                print(f"Error adding data to the database: {e}")
            
        def total(self):
            self.total = self.wides+self.no+self.lb+self.b
            return self.total

            
            

    def close_database(self):
        conn.close()
            
            
            

            
        

















