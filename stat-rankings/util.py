import numpy as np
from trueskill import Rating, quality_1vs1, rate_1vs1 
import pandas as pd
from collections import *
import csv

gamedirs = ['../data/64/Singles/','../data/Melee/Singles/', '../data/Brawl/Singles/', '../data/Smash4/Singles/']
sixtyfour_dir = '64'
melee_dir = 'Melee'
brawl_dir = 'Brawl'
smash4_dir = 'Smash4'
game_dirs = {1: sixtyfour_dir, 2: melee_dir, 3: smash4_dir}

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

def get_filename(game, tourney, typeof):
    return('../data/' + game_dirs[int(game)] + '/Singles/' + tourney + typeof)

def read_placements(game, tourney, players):
    with open(get_filename(game, tourney, '-standings.csv')) as stream:
        has_header = csv.Sniffer().has_header(stream.read(1024))
        stream.seek(0)  # rewind
        incsv = csv.reader(stream)
        if has_header:
            next(incsv)  # skip header row

        for placement_data in incsv:
            players[placement_data[0]].placement = placement_data[1]

    return players


def tourneys_reader(location):
    #Get tournaments in sorted order.
    first = 1
    with open(location) as stream:
        has_header = csv.Sniffer().has_header(stream.read(1024))
        stream.seek(0)  # rewind
        incsv = csv.reader(stream)
        if has_header:
            next(incsv)  # skip header row
        column = 1
        for tourney_data in incsv:
            if first:
                tnmt_array = np.array([tourney_data[1], tourney_data[3], tourney_data[4]])
                tnmt_array.shape = (1,3)
                first = 0
            else:
                tnmt_array = np.append(tnmt_array, np.array([tourney_data[1], tourney_data[3], tourney_data[4]]).reshape(1,3), axis = 0)
    return tnmt_array[tnmt_array[:,1].argsort()]


def filter_match_placing(threshold, players, p1, p2):
    if(threshold == -1):
        return False;
    if(int(players[p1].placement) > threshold or int(players[p2].placement) > threshold):
        return True;
    return False;


def check_valid_match(set_data):
    if(int(set_data[3]) == -1 or int(set_data[4]) == -1):
        return False
    return True

class Player:
    def __init__(self, name):
        self.name = name
        self.rating = Rating()
        self.num_tournaments = 0
        self.placement = 1000
        self.num_sets = 0
        self.wlr = [0, 0]

class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )
        else:
            ret = self[key] = self.default_factory(key)
        return ret
