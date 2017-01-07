import numpy as np

gamedirs = {'64': '../data/64/Singles/', 'melee': '../data/Melee/Singles/'}

def sanatize_name(name):
    return name.lower().strip()

player_name = sanatize_name(raw_input("Enter the Player's Name:\n"))
game = gamedirs[raw_input("Enter the Player's Game:\n")]

tournaments = np.loadtxt(game + 'tournaments.csv', dtype={'names': ['slug', 'date-start', 'date-end', 'entrants'], 'formats' : ['S64', 'S16', 'S16', 'i4']}, delimiter = ",", skiprows = 1, ndmin = 2)

for tourney in tournaments:
    tourney_filename = game + tourney['slug'][0] + '-sets.csv'
    with open(tourney_filename, 'r') as f:
        for line in f:
            set_info = line.split(',')
            if(set_info[0] == player_name or set_info[1] == player_name):
                print(set_info)
