import numpy as np

gamedirs = {'64': '../data/64/Singles/', 'melee': '../data/Melee/Singles/'}

def sanatize_name(name):
    return name.lower().strip()

player_name = sanatize_name(raw_input("Enter the Player's Name:\n"))
game = gamedirs[raw_input("Enter the Player's Game:\n")]

tournaments = np.loadtxt(game + 'tournaments.csv', dtype={'names': ['slug', 'date-start', 'date-end', 'entrants'], 'formats' : ['S64', 'S16', 'S16', 'i4']}, delimiter = ",", skiprows = 1, ndmin = 2)

beat = []
lost = []

for tourney in tournaments:
    tourney_filename = game + tourney['slug'][0] + '-sets.csv'
    with open(tourney_filename, 'r') as f:
        for line in f:
            set_info = line.split(',')
            if(set_info[0] == player_name):
                #print(type(set_info[2]))
                if(int(set_info[2]) == 0):
                    beat.append(set_info[1])
                else:
                    lost.append(set_info[1])
            elif(set_info[1] == player_name):
                #print(type(set_info[2]))
                if(int(set_info[2]) == 1):
                    beat.append(set_info[0])
                else:
                    lost.append(set_info[0])

print(player_name + "won against:\n")
print(beat)
print(player_name + "lost against:\n")
print(lost)
