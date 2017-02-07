from collections import *
import csv
import numpy as np
from util import *

# Trueskill Implementation courtesy of http://trueskill.org/

all_players = keydefaultdict(Player)
all_matches = []
game = raw_input("What game would you like to generate TrueSkill Rankings for? \n1: 64 \n2: Melee \n3: Smash4\n")
threshold = raw_input("Would you like to enforce a threshold on placings? (-1 = no, otherwise enter the minimum placing to count the match)\n")

#Get tournaments in sorted order.
sorted_tourneys = tourneys_reader('../data/' + game_dirs[int(game)] + '/Singles/tournaments.csv')

for tourney in sorted_tourneys:
    current_matches = []
    current_players = np.array([])

    all_players = read_placements(game, tourney[0], all_players)

    with open(get_filename(game, tourney[0], '-sets.csv')) as stream:
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
            if(not check_valid_match(set_data)):
                continue

            if(filter_match_placing(int(threshold), all_players, set_data[0], set_data[1])):
                continue

            #Update the number of sets and win/loss
            all_players[set_data[0]].num_sets += 1
            all_players[set_data[1]].num_sets += 1
            winner = int(set_data[2])
            all_players[set_data[winner]].rating, all_players[set_data[1 - winner]].rating = rate_1vs1(all_players[set_data[winner]].rating,all_players[set_data[1 - winner]].rating)
            all_players[set_data[winner]].wlr[0] += 1
            all_players[set_data[1 - winner]].wlr[1] += 1


rankings = np.array([]).reshape(0,6)
for player in all_players:
    rankings = np.append(rankings, np.array([player, all_players[player].rating.mu, all_players[player].rating.sigma,all_players[player].wlr[0],all_players[player].wlr[1], all_players[player].num_sets]).reshape(1,6), axis=0)

final = rankings[rankings[:,1].argsort()[::-1]]
f = open(game_dirs[int(game)] + "SinglesTrueSkill.csv", 'w')
f.write("player,mu,sigma,wins,losses,sets\n")
for pl in final:
    f.write(",".join(pl) + '\n')

f.close()
