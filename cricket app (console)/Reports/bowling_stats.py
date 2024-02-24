import sqlite3
import os

# getting path of the db
db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'your_database.db'))

def get_player_bowling_stats(player_name):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    try:
        # Use a JOIN statement to retrieve player bowling stats for all matches
        cursor.execute('''
            SELECT
                Player.id,
                Player.name AS player_name,
                COUNT(Over.id) AS total_overs,
                SUM(Over.score) AS total_score,
                MAX(Over.wickets) AS max_wickets
            FROM
                Player
                LEFT JOIN Over ON Player.id = Over.player_id
            WHERE
                Player.name = ?
            GROUP BY
                Player.id, player_name
        ''', (player_name,))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            player_id = result[0]
            player_name = result[1]
            stats = {
                'totalOvers': result[2],
                'totalScore': result[3],
                'maxWickets': result[4]
            }
            
            # Fetching the details of the best performance in a specific match
            bestfigure = cursor.execute('''
                SELECT
                    MAX(Over.wickets) AS best_wickets,
                    SUM(Over.score) AS best_score,
                    CASE
                        WHEN Match.team_one_id = ? THEN (SELECT team_name FROM Team WHERE id = Match.team_two_id)
                        ELSE (SELECT team_name FROM Team WHERE id = Match.team_one_id)
                    END AS opponent_team_name
                FROM
                    Over
                    JOIN Match ON Over.match_id = Match.id
                WHERE
                    Over.player_id = ?
                GROUP BY
                    Over.match_id
                ORDER BY
                    best_wickets DESC, best_score ASC
                LIMIT 1
            ''', (player_id, player_id))

            best_performance = bestfigure.fetchone()

            if best_performance:
                stats['bestWickets'] = best_performance[0]
                stats['bestScore'] = best_performance[1]
                stats['opponentTeamName'] = best_performance[2]

            return {'playerName': player_name, 'playerId': player_id, 'stats': stats}
        else:
            return None

    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None

    finally:
        conn.close()

# Example usage for a specific player (e.g., 'John')
player_name = input('Enter player name: ')
player_bowling_stats = get_player_bowling_stats(player_name)

if player_bowling_stats:
    print(f"Aggregated bowling stats for {player_bowling_stats['playerName']} (Player ID {player_bowling_stats['playerId']}):")
    print('overs     runs     Economy     wickets     BF')
    
    ec = int(player_bowling_stats['stats']['totalScore']) / int(player_bowling_stats['stats']['totalOvers'])
    print(f"{player_bowling_stats['stats']['totalOvers']}         {player_bowling_stats['stats']['totalScore']}       {ec:.2f}    {player_bowling_stats['stats']['maxWickets']}")
    
    if 'bestWickets' in player_bowling_stats['stats']:
        print(f"Best Bowling Figure: {player_bowling_stats['stats']['bestWickets']}/{player_bowling_stats['stats']['bestScore']} against {player_bowling_stats['stats']['opponentTeamName']}")
else:
    print(f"No bowling stats found for {player_name}")
