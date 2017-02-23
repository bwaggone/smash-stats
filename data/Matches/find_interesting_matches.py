import sys
import os
sys.path.append("../../stat-rankings")
import numpy as np
from collections import *
import csv
from util import *
sixtyfour_dir = './64/Singles/'
melee_dir = './Melee/Singles/'
brawl_dir = './Brawl/Singles/'
smash4_dir = './Smash4/Singles/'


game = raw_input("What game do you want to find interesting matches for?")
game = int(game)

def write_match(p1, p2, match_file, t_slug, t_name):
    match_file.write(t_name + ',' + t_slug + ',' + p1 + ',' + p2 + '\n')
    return

#Get Players on the Official Ranking List
ranks = defaultdict(int)
first = 1
with open('../rankings/' + game_dirs[game] + '-rankings.csv') as stream:
    has_header = csv.Sniffer().has_header(stream.read(1024))
    stream.seek(0)  # rewind
    incsv = csv.reader(stream)
    if has_header:
        next(incsv)  # skip header row
    column = 1
    for ranking_data in incsv:
        ranks[ranking_data[0].lower()] = ranking_data[1];
    

#Get tournaments in sorted order.
first = 1
with open('../' + game_dirs[game] + '/Singles/tournaments.csv') as stream:
    has_header = csv.Sniffer().has_header(stream.read(1024))
    stream.seek(0)  # rewind
    incsv = csv.reader(stream)
    if has_header:
        next(incsv)  # skip header row
    column = 1
    tnmt_array = np.array([]).reshape(0,4)
    for tourney_data in incsv:
        tnmt_array = np.append(tnmt_array, np.array([tourney_data[1], tourney_data[3], tourney_data[4], tourney_data[0]]).reshape(1,4), axis = 0)

sorted_tourneys = tnmt_array[tnmt_array[:,1].argsort()[::-1]]

match_file = game_dirs[game] + "-matches.csv"
up_file = open(match_file,"w")
up_file.write("Tournament,slug,Player 1, Player 2\n")
iteration = 0
for tourney in sorted_tourneys:
    with open('../' + game_dirs[game] + '/Singles/' + tourney[0] + '-sets.csv') as stream:
        if(iteration > 4):
            continue
        print(tourney[0], tourney[3])
        has_header = csv.Sniffer().has_header(stream.read(1024))
        stream.seek(0)  # rewind
        incsv = csv.reader(stream)
        if has_header:
            next(incsv)  # skip header row
        iteration += 1
        for set_data in incsv:
            #set_data[0] is p1
            #set_data[1] is p2
            #set_data[2] is winner/loser
            #set_data[3-4] is the game count. If either is -1, do not report.

            #Check if the set was a DQ
            if(not check_valid_match(set_data)):
                continue

            p1rank = int(ranks[set_data[0]])
            p2rank = int(ranks[set_data[1]])
            if((p1rank == 0 or p2rank == 0) and not(p1rank == p2rank)):

                if((p1rank == 0 and (int(set_data[2]) == 0)) or (p2rank == 0 and (int(set_data[2]) == 1))):
                    write_match(set_data[0], set_data[1], up_file, tourney[0], tourney[3])
                    #print(set_data, p1rank, p2rank)

            elif((p1rank != 0 and p2rank != 0) and (abs(p1rank - p2rank) > 10)):
                if(p1rank > p2rank and not int(set_data[2]) or (p1rank < p2rank) and int(set_data[2])):
                    write_match(set_data[0], set_data[1], up_file, tourney[0], tourney[3])
                    #print(set_data, p1rank, p2rank, set_data[2])

            elif((p1rank <= 25) and (p2rank <= 25) and (int(set_data[4]) + int(set_data[3])) == 5):
                    write_match(set_data[0], set_data[1], up_file, tourney[0], tourney[3])
                    #print(set_data, p1rank, p2rank, set_data[2])


