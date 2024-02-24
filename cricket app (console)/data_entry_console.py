import sampleData as data
import datetime
def main():

    menu = """
    a) add players
    t) add teams
    q) quit
    """
    print(menu)
    while True:
        choice = input("Enter your choice: ")

        if choice == 'a':

            player = input('Enter player name, team_id, age, role by comma separating values: ').split(',')
            player_name = player[0]
            player_team_id = player[1]
            age = player[2]
            role = player[3].upper()
            a = data.add_player(player_name,player_team_id,age,role)
            a.add_to_database()
        if choice == 't':
            team_name = input('Enter teams name: ').split(',')
            for i in team_name:
                date_registered = datetime.datetime.now().strftime('%Y-%m-%d')
                a = data.register_team(i,date_registered)
                a.add_to_database()
        elif choice =='q':
            data.close_database()
            print('Quit!')
            break
main()
