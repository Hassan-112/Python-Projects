import sampleData as data
import sqlite3 as sq
import datetime

conn = sq.connect('your_database.db')
cursor = conn.cursor()


class Match:
    def match_start():
        cricket_instance = data.cricket()
        cursor.execute("SELECT MAX(id) FROM Match")
        max_match_id = cursor.fetchone()[0]

        if max_match_id is not None:
            match_id = max_match_id + 1
        else:
            match_id = 1

        cursor.execute(f'SELECT id,team_name FROM Team')
        print("===============================")
        print("Team_Id       Team_Name")
        print("===============================")
        for i in cursor:
            print(str(i[0]).ljust(7), "=".ljust(5), i[1])
        print("===============================")
        print('\n')
        print('First enter the idea of team which is batting first.')
        while True:
            try:
                team_one_id = int(input('Enter team one id: '))
                team_two_id = int(input('Enter team two id: '))
                break  # Break out of the loop if both inputs are valid
            except ValueError:
                print('Invalid input, id must be an integer. Please try again.')
        while True:
            try:
                overs = int(input('Enter total overs: '))
                break
            except ValueError:
                print('Overs must be an integer')
        date_held = datetime.datetime.now().strftime('%Y-%m-%d')
        team1 = cursor.execute("SELECT team_name FROM Team WHERE id = ?", (team_one_id,)).fetchone()
        team2 = cursor.execute("SELECT team_name FROM Team WHERE id = ?", (team_two_id,)).fetchone()
        cursor.execute(f'SELECT id, name FROM Player WHERE team_id={team_one_id}')
        print(f'\n{team1} players ids:')
        players1 = []
        team_one_players = list(cursor)
        length1 = len(team_one_players)

        for index, i in enumerate(team_one_players):
            print(f"[{i[1]}: {i[0]}]", end='')
            players1.append(i[0])

            if index < length1 - 1:
                print(',', end='')

        print()

        print('\n')

        print(f'{team2} players ids:')
        players2 = []
        cursor.execute(f'SELECT id, name FROM Player WHERE team_id=={team_two_id}')
        team_two_players = list(cursor)
        length2 = len(team_two_players)
        for index, i in enumerate(team_two_players):
            print(f"[{i[1]}: {i[0]}]", end='')
            players2.append(i[0])

            if index < length2 - 1:
                print(',', end='')

        print()

        sum = 0
        team_one_outs = 0
        print(f'\n{team2} Bowling:')
        balls1 = 0
        consecutive = False
        completion = False
        for i in range(overs):
            while True:
                try:
                    while True:
                        id_found = False
                        while True:
                            player_id = int(input('Enter bowler id: '))
                            if player_id == consecutive:

                                if consecutive:
                                    print('A bowler cannot throw consecutive overs!')
                            else:
                                break

                        for j in range(len(players2)):
                            if player_id == players2[j]:
                                id_found = True
                                break
                        if id_found:
                            break
                        else:
                            print('Enter bowler id again: ')
                    score = int(input(f'Enter score in over{i+1}: '))

                    while True:
                        while True:
                            wickets = int(input('Enter wickets in the over: '))
                            if wickets > 6:
                                print("It won't be possible more than six wickets in an over, write the correct wickets again!")
                            else:
                                break
                        if team_one_outs + wickets <= 10:
                            break
                        else:
                            print('Too much wickets, wickets exceeding 10 which is not possible')

                    break
                except ValueError:
                    print('Invalid value. please write again the over detail')

            team_one_outs += wickets
            sum += score
            if team_one_outs == 10:
                while True:
                    try:
                        while True:
                            ball = int(input('Enter total balls bowled in this over: '))
                            if ball > 6:
                                print('Invalid balls, balls must be less than 7')
                            else:
                                break
                        break
                    except ValueError:
                        print('Invalid balls balls must be i')

                balls1 += ball
                over_instance = cricket_instance.over(player_id, match_id, score, team_two_id, wickets)
                over_instance.add_to_database()

                print('Team all out')
                break
            balls1 += 6

            over_instance = cricket_instance.over(player_id, match_id, score, team_two_id, wickets)
            over_instance.add_to_database()
            completion = True
            if completion:
                consecutive = player_id
        print(f'\n{team1} extras: ')
        while True:
            try:
                wides = int(input('Enter wides: '))
                no = int(input('Enter no: '))
                b = int(input('Enter byes: '))
                lb = int(input('Enter leg byes: '))
                break
            except ValueError:
                print("Invalid extras data, Extras must be integer type data")

        total_extras_score_team_one = wides + no + b + lb
        extras = cricket_instance.extras(match_id, team_one_id, wides, no, lb, b)
        extras.add_to_database()

        id_found = False
        duplicate = False
        batted1 = []

        # batting stats
        print(f'\n{team1} batting: ')
        for i in range(team_one_outs + 2):
            while True:
                try:
                    player_id = int(input('Enter batsman id: '))
                    if player_id not in players1:
                        print("The id does not exist in the team")
                        continue  # Continue to the next iteration
                    if player_id in batted1:
                        print('Player stats already entered!')
                        continue  # Continue to the next iteration

                    batted1.append(player_id)

                    while True:
                        try:
                            score = int(input('Score: '))
                            break
                        except ValueError:
                            print("Invalid score, score must be of int type")

                    while True:
                        try:
                            while True:
                                try:
                                    balls = int(input('Balls: '))
                                    if balls < 0 or (balls == 0 and score > 1):
                                        print('Invalid balls, enter balls again: ')
                                    else:
                                        break
                            
                                except ValueError:
                                    print("Invalid balls, balls must be of int type")
                            break
                        except ZeroDivisionError:
                            print('Invalid division by zero. Please enter a non-zero value for balls')



                    while True:
                        try:
                            while True:
                                sixes = int(input('Sixes: '))
                                # Validate sixes
                                if sixes * 6 > score:
                                    print('Sixes data is not valid, enter sixes again: ')
                                else:
                                    break
                            break
                        except ValueError:
                            print("Sixes must be int")

                    while True:
                        try:
                            while True:
                                fours = int(input('Fours: '))
                                # Validate fours
                                if fours * 4 + sixes * 6 > score:
                                    print('Fours data is not valid, enter fours again: ')
                                else:
                                    break
                            break
                        except ValueError:
                            print("Fours must be int")

                    # Validate dots
                    dots = 0
                    if sixes + fours != balls:
                        while True:
                            try:
                                dots = int(input('Dots: '))
                                break
                            except ValueError:
                                print("Dots must be int")
                    break
                except ValueError:
                    print('Player ID must be of int type and should exist in the team. Enter data again')

            # Assuming you have a Cricket class with a method batting_stats
            batting = cricket_instance.batting_stats(player_id, match_id, score, balls, sixes, fours, dots, team_one_id)
            batting.add_to_database()

            # Exit loop after 10 entries
            if i == 10:
                break


        team_one_score = sum
        print(f'\nTeam2 extras: ')
        while True:
            try:
                wides = int(input('Enter wides: '))
                no = int(input('Enter no: '))
                b = int(input('Enter byes: '))
                lb = int(input('Enter leg byes: '))
                break
            except ValueError:
                print("Invalid extras data, Extras must be integer type data")
        total_extras_score_team_two = wides + no + b + lb
        extras = cricket_instance.extras(match_id, team_two_id, wides, no, lb, b)
        extras.add_to_database()
        sum = 0
        team_two_outs = 0
        print(f'\n{team2} Bowling:')
        balls2 = 0
        consecutive = False
        completion = False
        for i in range(overs):
            while True:
                try:
                    while True:
                        id_found = False
                        while True:
                            player_id = int(input('Enter bowler id: '))
                            if player_id == consecutive:

                                if consecutive:
                                    print('A bowler cannot throw consecutive overs!')
                            else:
                                break

                        for j in range(len(players2)):
                            if player_id == players2[j]:
                                id_found = True
                                break
                        if id_found:
                            break
                        else:
                            print('Enter bowler id again: ')
                    score = int(input(f'Enter score in over{i+1}: '))

                    while True:
                        while True:
                            wickets = int(input('Enter wickets in the over: '))
                            if wickets > 6:
                                print("It won't be possible more than six wickets in an over, write the correct wickets again!")
                            else:
                                break
                        if team_two_outs + wickets <= 10:
                            break
                        else:
                            print('Too much wickets, wickets exceeding 10 which is not possible')

                    break
                except ValueError:
                    print('Invalid value. please write again the over detail')

            team_two_outs += wickets
            sum += score
            if team_two_outs == 10:
                while True:
                    try:
                        while True:
                            ball = int(input('Enter total balls bowled in this over: '))
                            if ball > 6:
                                print('Invalid balls, balls must be less than 7')
                            else:
                                break
                        break
                    except ValueError:
                        print('Invalid balls balls must be i')

                balls2 += ball
                over_instance = cricket_instance.over(player_id, match_id, score, team_two_id, wickets)
                over_instance.add_to_database()

                print('Team all out')
                break
            balls2 += 6

            over_instance = cricket_instance.over(player_id, match_id, score, team_two_id, wickets)
            over_instance.add_to_database()
            completion = True
            if completion:
                consecutive = player_id

        print(f'\n{team2} batting: ')
        batted2 = []
        for i in range(team_two_outs + 2):
            while True:
                try:
                    player_id = int(input('Enter batsman id: '))
                    if player_id not in players2:
                        print("The id does not exist in the team")
                        continue  # Continue to the next iteration
                    if player_id in batted2:
                        print('Player stats already entered!')
                        continue  # Continue to the next iteration

                    batted2.append(player_id)

                    while True:
                        try:
                            score = int(input('Score: '))
                            break
                        except ValueError:
                            print("Invalid score, score must be of int type")

                    while True:
                        try:
                            while True:
                                try:
                                    balls = int(input('Balls: '))
                                    if balls < 0 or (balls == 0 and score > 1):
                                        print('Invalid balls, enter balls again: ')
                                    else:
                                        break
                            
                                except ValueError:
                                    print("Invalid balls, balls must be of int type")
                            break
                        except ZeroDivisionError:
                            print('Invalid division by zero. Please enter a non-zero value for balls')



                    while True:
                        try:
                            while True:
                                sixes = int(input('Sixes: '))
                                # Validate sixes
                                if sixes * 6 > score:
                                    print('Sixes data is not valid, enter sixes again: ')
                                else:
                                    break
                            break
                        except ValueError:
                            print("Sixes must be int")

                    while True:
                        try:
                            while True:
                                fours = int(input('Fours: '))
                                # Validate fours
                                if fours * 4 + sixes * 6 > score:
                                    print('Fours data is not valid, enter fours again: ')
                                else:
                                    break
                            break
                        except ValueError:
                            print("Fours must be int")

                    # Validate dots
                    dots = 0
                    if sixes + fours != balls:
                        while True:
                            try:
                                dots = int(input('Dots: '))
                                break
                            except ValueError:
                                print("Dots must be int")
                    break
                except ValueError:
                    print('Player ID must be of int type and should exist in the team. Enter data again')

            # Assuming you have a Cricket class with a method batting_stats
            batting = cricket_instance.batting_stats(player_id, match_id, score, balls, sixes, fours, dots, team_two_id)
            batting.add_to_database()

            # Exit loop after 10 entries
            if i == 10:
                break

        team_two_score = sum
        match_instance = cricket_instance.match(overs, team_one_id, team_two_id, team_one_outs, team_two_outs, date_held, balls1, balls2)
        match_instance.add_to_database()

        print("Match Starts!")


Match.match_start()
