import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import sqlite3 as sq
import datetime
conn = sq.connect('your_database.db')
cursor = conn.cursor()
class CricketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cricket App")

        self.tab_control = ttk.Notebook(self.root)

        self.player_tab = ttk.Frame(self.tab_control)
        self.team_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.player_tab, text="Add Players")
        self.tab_control.add(self.team_tab, text="Add Teams")

        self.tab_control.pack(expand=1, fill="both")

        # Initialize variables
        self.player_name_var = tk.StringVar()
        self.selected_team_var = tk.StringVar()
        self.age_var = tk.IntVar()
        self.role_var = tk.StringVar()

        self.team_name_var = tk.StringVar()

        self.create_player_tab()
        self.create_team_tab()

    def create_player_tab(self):
        # Player Tab
        player_label = ttk.Label(self.player_tab, text="Player Entry", font=("Helvetica", 16))
        player_label.grid(row=0, column=0, pady=10)

        player_name_label = ttk.Label(self.player_tab, text="Player Name:")
        player_name_label.grid(row=1, column=0, sticky="E", padx=10)

        player_name_entry = ttk.Entry(self.player_tab, textvariable=self.player_name_var)
        player_name_entry.grid(row=1, column=1, padx=10, pady=5)

        team_label = ttk.Label(self.player_tab, text="Select Team:")
        team_label.grid(row=2, column=0, sticky="E", padx=10)

        # Fetch team names from the database
        self.team_combobox = ttk.Combobox(self.player_tab, textvariable=self.selected_team_var)
        self.team_combobox.grid(row=2, column=1, padx=10, pady=5)

        age_label = ttk.Label(self.player_tab, text="Age:")
        age_label.grid(row=3, column=0, sticky="E", padx=10)

        age_entry = ttk.Entry(self.player_tab, textvariable=self.age_var)
        age_entry.grid(row=3, column=1, padx=10, pady=5)

        role_label = ttk.Label(self.player_tab, text="Role:")
        role_label.grid(row=4, column=0, sticky="E", padx=10)

        # Dropdown menu for selecting player role
        role_combobox = ttk.Combobox(self.player_tab, textvariable=self.role_var, values=["AR", "BOWLEER", "BATSMAN"])
        role_combobox.grid(row=4, column=1, padx=10, pady=5)

        search_button = ttk.Button(self.player_tab, text="Search Teams", command=self.search_teams)
        search_button.grid(row=2, column=2, padx=10, pady=5)

        add_button = ttk.Button(self.player_tab, text="Add Player", command=self.add_player)
        add_button.grid(row=5, column=1, pady=10)

        # Set completion list for team_combobox
        self.set_completion_list(self.team_combobox, self.get_team_names())

    def create_team_tab(self):
        # Team Tab
        team_label = ttk.Label(self.team_tab, text="Team Entry", font=("Helvetica", 16))
        team_label.grid(row=0, column=0, pady=10)

        team_name_label = ttk.Label(self.team_tab, text="Team Name:")
        team_name_label.grid(row=1, column=0, sticky="E", padx=10)

        team_name_entry = ttk.Entry(self.team_tab, textvariable=self.team_name_var)
        team_name_entry.grid(row=1, column=1, padx=10, pady=5)

        add_button = ttk.Button(self.team_tab, text="Add Team", command=self.add_team)
        add_button.grid(row=2, column=1, pady=10)

    def add_player(self):
        player_name = self.player_name_var.get()
        selected_team_name = self.selected_team_var.get()
        age = self.age_var.get()
        role = self.role_var.get()

        # Fetch team id based on selected team name
        cursor.execute(f"SELECT id FROM Team WHERE team_name = ?", (selected_team_name,))
        team_id = cursor.fetchone()[0]

        # Insert player data into the database
        cursor.execute("INSERT INTO Player (name, age, team_id, role) VALUES (?, ?, ?, ?)",
                       (player_name, age, team_id, role.upper()))

        # Commit the changes
        conn.commit()

        messagebox.showinfo("Success", "Player added successfully!")

    def add_team(self):
        team_name = self.team_name_var.get()
        date_registered = datetime.datetime.now().strftime('%Y-%m-%d')

        # Insert team data into the database
        cursor.execute("INSERT INTO Team (team_name, date_registered) VALUES (?, ?)",
                       (team_name, date_registered))

        # Commit the changes
        conn.commit()

        messagebox.showinfo("Success", "Team added successfully!")

    def search_teams(self):
        search_term = self.team_combobox.get().lower()
        filtered_teams = [team for team in self.get_team_names() if search_term in team.lower()]

        self.set_completion_list(self.team_combobox, filtered_teams)

    def set_completion_list(self, combobox, completion_list):
        combobox['values'] = completion_list

    def get_team_names(self):
        cursor.execute("SELECT team_name FROM Team")
        teams = cursor.fetchall()
        return [team[0] for team in teams]


def main():
    root = tk.Tk()
    app = CricketApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
