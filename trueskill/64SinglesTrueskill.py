from collections import *
from trueskill import Rating, quality_1vs1, rate_1vs1 
import csv
import numpy as np

# Trueskill Implementation courtesy of http://trueskill.org/


sixtyfour_dir = '../data/64/Singles/'
melee_dir = '../data/Melee/Singles/'
brawl_dir = '../data/Brawl/Singles/'
smash4_dir = '../data/Smash4/Singles/'


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )
        else:
            ret = self[key] = self.default_factory(key)
        return ret

class Player:
    def __init__(self, name):
        self.name = name
        self.rating = Rating()
        self.num_tournaments = 0
        self.num_sets = 0
        self.wlr = [0, 0]


all_players = keydefaultdict(Player)
all_matches = []



#Get tournaments in sorted order.
first = 1
with open(sixtyfour_dir + 'tournaments.csv') as stream:
    has_header = csv.Sniffer().has_header(stream.read(1024))
    stream.seek(0)  # rewind
    incsv = csv.reader(stream)
    if has_header:
        next(incsv)  # skip header row
    column = 1
    for tourney_data in incsv:
        if first:
            tnmt_array = np.array([tourney_data[0], tourney_data[2], tourney_data[3]])
            tnmt_array.shape = (1,3)
            first = 0
        else:
            tnmt_array = np.append(tnmt_array, np.array([tourney_data[0], tourney_data[2], tourney_data[3]]).reshape(1,3), axis = 0)

sorted_tourneys = tnmt_array[tnmt_array[:,1].argsort()]




for tourney in sorted_tourneys:
    #if(tourney[0] == "wtfox-2"):
    #    print("skipped")
    #    continue
    current_matches = []
    current_players = np.array([])
    with open(sixtyfour_dir + tourney[0] + '-sets.csv') as stream:
        has_header = csv.Sniffer().has_header(stream.read(1024))
        stream.seek(0)  # rewind
        incsv = csv.reader(stream)
        if has_header:
            next(incsv)  # skip header row
        column = 1
        for set_data in incsv:
            #set_data[0] is p1
            #set_data[1] is p2
            #set_data[2] is winner/loser
            #set_data[3-4] is the game count. If either is -1, do not report.

            p1 = all_players[set_data[0]]
            p2 = all_players[set_data[1]]

            #Check if the set was a DQ
            if(int(set_data[3]) == -1 or int(set_data[4] == -1)):
                continue

            #Update the number of sets and win/loss
            all_players[set_data[0]].num_sets += 1
            all_players[set_data[1]].num_sets += 1
            
            if(not int(set_data[2])):
                all_players[set_data[0]].rating, all_players[set_data[1]].rating = rate_1vs1(all_players[set_data[0]].rating,all_players[set_data[1]].rating)
                all_players[set_data[0]].wlr[0] += 1
                all_players[set_data[1]].wlr[1] += 1
            else:
                all_players[set_data[1]].rating, all_players[set_data[0]].rating = rate_1vs1(all_players[set_data[1]].rating,all_players[set_data[0]].rating)
                all_players[set_data[1]].wlr[0] += 1
                all_players[set_data[0]].wlr[1] += 1


first = 1
for player in all_players:
    if first:
        first = 0
        rankings = np.array([player, all_players[player].rating.mu, all_players[player].rating.sigma,all_players[player].wlr[0],all_players[player].wlr[1], all_players[player].num_sets]).reshape(1,6)
    else:
        rankings = np.append(rankings, np.array([player, all_players[player].rating.mu, all_players[player].rating.sigma,all_players[player].wlr[0],all_players[player].wlr[1], all_players[player].num_sets]).reshape(1,6), axis=0)

final = rankings[rankings[:,1].argsort()[::-1]]
f = open("64SinglesTrueSkill.csv", 'w')
f.write("player,mu,sigma,wins,losses,sets\n")
for pl in final:
    f.write(",".join(pl) + '\n')

f.close()

