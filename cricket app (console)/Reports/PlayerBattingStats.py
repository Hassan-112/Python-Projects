import sqlite3
import os

# getting path of the db
db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'your_database.db'))

def get_aggregated_player_stats():
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    try:
        # Use a JOIN statement to retrieve player batting stats
        cursor.execute('''
            SELECT
                Player.id,
                Player.name AS player_name,
                SUM(BattingStats.score) AS total_score,
                SUM(BattingStats.sixes) AS total_sixes,
                SUM(BattingStats.balls) AS total_balls,
                SUM(BattingStats.dots) AS total_dots,
                SUM(BattingStats.fours) AS total_fours,
                (SUM(BattingStats.score) * 1.0 / NULLIF(SUM(BattingStats.balls), 0) * 100) AS strike_rate
            FROM
                Player
                JOIN BattingStats ON Player.id = BattingStats.player_id
            GROUP BY
                Player.id, player_name
        ''')

        # Fetch the results
        results = cursor.fetchall()

        aggregated_stats = {}
        for result in results:
            player_id = result[0]
            player_name = result[1].lower()  # Convert to lowercase for case-insensitive comparison
            stats = {
                'totalScore': result[2],
                'totalSixes': result[3],
                'totalBalls': result[4],
                'totalDots': result[5],
                'totalFours': result[6],
                'strikeRate': result[7]
            }
            aggregated_stats[player_name] = {'playerId': player_id, 'stats': stats}

        return aggregated_stats

    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None

    finally:
        conn.close()

def get_aggregated_stats_for_player(player_name):
    player_stats = get_aggregated_player_stats()

    if player_stats and player_name.lower() in player_stats:
        data = player_stats[player_name.lower()]
        player_id = data['playerId']
        stats = data['stats']
        
        print(f"stats for {player_name}:")
        print('============================================')
        print('S       B      6s      4s      D      SR')
        print('============================================')
        print(f'{stats['totalScore']}      {stats['totalBalls']}     {stats['totalSixes']}      {stats['totalFours']}      {stats['totalDots']}     {stats['strikeRate']:.2f}')
        print('============================================')
        
    else:
        print(f"No batting stats found for {player_name}")

player = input('Enter player name: ')
get_aggregated_stats_for_player(player)
