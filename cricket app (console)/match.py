import sampleData as data
import sqlite3 as sq
import datetime

conn = sq.connect('your_database.db')
cursor = conn.cursor()


class Match:
    @staticmethod
    def print_team_table(cursor):
        print("===============================")
        print("Team_Id       Team_Name")
        print("===============================")
        for i in cursor:
            print(str(i[0]).ljust(7), "=".ljust(5), i[1])
        print("===============================")

    @staticmethod
    def get_valid_input(prompt, data_type=int):
        while True:
            try:
                value = data_type(input(prompt))
                break
            except ValueError:
                print(f'Invalid input, {prompt} must be {data_type.__name__}. Please try again.')
        return value

    @staticmethod
    def enter_extras():
        wides = Match.get_valid_input('Enter wides: ')
        no = Match.get_valid_input('Enter no: ')
        b = Match.get_valid_input('Enter byes: ')
        lb = Match.get_valid_input('Enter leg byes: ')
        return wides, no, b, lb

    @staticmethod
    def enter_player_stats(players, batted, team_id):
        while True:
            try:
                player_id = Match.get_valid_input('Enter batsman id: ')
                if player_id not in players:
                    print("The id does not exist in the team")
                    continue
                if player_id in batted:
                    print('Player stats already entered!')
                    continue

                batted.append(player_id)
                score = Match.get_valid_input('Score: ')
                balls = Match.get_valid_input('Balls: ')
                sixes = Match.get_valid_input('Sixes: ')
                fours = Match.get_valid_input('Fours: ')
                dots = Match.get_valid_input('Dots: ')
                # Validate sixes
                if sixes * 6 > score or fours * 4 + sixes * 6 > score or (sixes + fours != balls):
                    print('Invalid input. Please enter data again.')
                    continue
                break
            except ValueError:
                print('Invalid input. Please enter data again.')

        return player_id, score, balls, sixes, fours, dots, team_id

    @staticmethod
    def enter_bowling_stats(players, consecutive):
        while True:
            try:
                player_id = Match.get_valid_input('Enter bowler id: ')
                if player_id == consecutive:
                    print('A bowler cannot bowl consecutive overs!')
                    continue
                if player_id not in players:
                    print('Invalid bowler id. Please enter again.')
                    continue
                score = Match.get_valid_input(f'Enter score: ')
                wickets = Match.get_valid_input('Enter wickets: ')
                # Validate wickets
                if wickets > 6:
                    print("It won't be possible more than six wickets in an over. Enter wickets again!")
                    continue
                break
            except ValueError:
                print('Invalid input. Please enter data again.')

        return player_id, score, wickets

    @staticmethod
    def match_start():
        cricket_instance = data.cricket()
        cursor.execute("SELECT MAX(id) FROM Match")
        max_match_id = cursor.fetchone()[0]

        match_id = max_match_id + 1 if max_match_id is not None else 1

        Match.print_team_table(cursor)

        team_one_id = Match.get_valid_input('Enter team one id: ')
        team_two_id = Match.get_valid_input('Enter team two id: ')
        overs = Match.get_valid_input('Enter total overs: ')

        date_held = datetime.datetime.now().strftime('%Y-%m-%d')

        team1 = cursor.execute("SELECT team_name FROM Team WHERE id = ?", (team_one_id,)).fetchone()
        team2 = cursor.execute("SELECT team_name FROM Team WHERE id = ?", (team_two_id,)).fetchone()

        players1 = Match.get_players_list(cursor, team_one_id)
        players2 = Match.get_players_list(cursor, team_two_id)

        sum, team_one_outs, balls1 = Match.enter_bowling_data(
            cricket_instance, team2, overs, players2, team_one_id, match_id
        )

        total_extras_score_team_one = Match.enter_extras_data(cricket_instance, match_id, team_one_id)

        batted1 = Match.enter_batting_data(cricket_instance, team1, players1, team_one_outs, match_id, 10, team_one_id)

        team_one_score = sum

        total_extras_score_team_two = Match.enter_extras_data(cricket_instance, match_id, team_two_id)

        sum, team_two_outs, balls2 = Match.enter_bowling_data(
            cricket_instance, team1, overs, players1, team_two_id, match_id
        )

        batted2 = Match.enter_batting_data(cricket_instance, team2, players2, team_two_outs, match_id, 10, team_two_id)

        team_two_score = sum

        Match.enter_match_data(cricket_instance, overs, team_one_id, team_two_id, team_one_outs, team_two_outs,
                               date_held, balls1, balls2, match_id)

        print("Match Starts!")

    @staticmethod
    def get_players_list(cursor, team_id):
        cursor.execute(f'SELECT id, name FROM Player WHERE team_id={team_id}')
        players = list(cursor)
        length = len(players)
        print(f'\nTeam players ids:')
        for index, i in enumerate(players):
            print(f"[{i[1]}: {i[0]}]", end='')
            if index < length - 1:
                print(',', end='')
        print()
        return [player[0] for player in players]

    @staticmethod
    def enter_bowling_data(cricket_instance, team, overs, players, team_id, match_id):
        sum = 0
        team_outs = 0
        print(f'\n{team} Bowling:')
        balls = 0
        consecutive = False
        completion = False
        for i in range(overs):
            while True:
                player_id, score, wickets = Match.enter_bowling_stats(players, consecutive)
                team_outs += wickets
                sum += score
                if team_outs == 10:
                    ball = Match.get_valid_input('Enter total balls bowled in this over: ')
                    balls += ball
                    over_instance = cricket_instance.over(player_id, match_id, score, team_id, wickets)
                    over_instance.add_to_database()
                    print('Team all out')
                    return sum, team_outs, balls
                balls += 6
                over_instance = cricket_instance.over(player_id, match_id, score, team_id, wickets)
                over_instance.add_to_database()
                completion = True
                if completion:
                    consecutive = player_id

    @staticmethod
    def enter_extras_data(cricket_instance, match_id, team_id):
        wides, no, b, lb = Match.enter_extras()
        total_extras_score = wides + no + b + lb
        extras = cricket_instance.extras(match_id, team_id, wides, no, lb, b)
        extras.add_to_database()
        return total_extras_score

    @staticmethod
    def enter_batting_data(cricket_instance, team, players, team_outs, match_id, max_entries, team_id):
        batted = []
        print(f'\n{team} Batting:')
        for i in range(team_outs + 2):
            player_id, score, balls, sixes, fours, dots, _ = Match.enter_player_stats(players, batted, team_id)
            batting = cricket_instance.batting_stats(player_id, match_id, score, balls, sixes, fours, dots, team_id)
            batting.add_to_database()
            if i == max_entries:
                break
        return batted

    @staticmethod
    def enter_match_data(cricket_instance, overs, team_one_id, team_two_id, team_one_outs, team_two_outs, date_held,
                         balls1, balls2, match_id):
        match_instance = cricket_instance.match(overs, team_one_id, team_two_id, team_one_outs, team_two_outs,
                                                date_held, balls1, balls2)
        match_instance.add_to_database()


Match.match_start()
