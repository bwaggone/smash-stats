import numpy as np
import pandas as pd

gamedirs = ['../data/64/Singles/','../data/Melee/Singles/', '../data/Brawl/Singles/', '../data/Smash4/Singles/']

#The following 3 functions are used to read the scrapped csv files

#PARAMETER INFORMATION

#"Game" refers to a game code passed in as an int.
# 0 = 64
# 1 = Melee
# 2 = Brawl
# 3 = Smash4

#"Tourney" refers to the tournament slug, passed in as a string

#Returns an X by 4 np matrix of tournament information
#def tourney_csvreader(game):
    #tmp = np.loadtxt(gamedirs[game] + 'tournaments.csv', dtype={'names': ['slug', 'date-start', 'date-end', 'entrants'], 'formats' : ['S32', 'S32', 'S32', 'i4']}, delimiter = ",", skiprows = 1, ndmin = 2)
    #return pd.read_csv(gamedirs[game] + 'tournaments.csv')
    #return np.genfromtxt(gamedirs[game] + 'tournaments.csv', dtype=None, delimiter = ",", usecols=[0,1,2,3], skip_header = 1)

#Returns an X by 5 matrix of set information for a tournament
def set_csvreader(game, tourney):
    return np.loadtxt(gamedirs[game] + tourney + '-sets.csv', dtype={'names': ('P1','P2','winner','P1Score','P2Score'), 'format' : ('S16', 'S16', 'i4', 'i4', 'i4')}, delimiter= ",", skiprows = 1)


#Returns a X by 2 matrix of gamertag and final placement 
def standing_csvreader(game, tourney):
    return np.loadtxt(gamedirs[game] + tourney + '-standings.csv', dtype={'names': ('player','result'), 'format' : ('S16', 'i4')}, delimiter= ",", skiprows = 1)
