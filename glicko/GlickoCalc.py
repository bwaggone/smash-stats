from glicko import *
import time
import datetime
import collections
import csv
import os
import numpy as np

sixtyfour_dir = '64'
melee_dir = 'Melee'
brawl_dir = 'Brawl'
smash4_dir = 'Smash4'
game_dirs = {1: sixtyfour_dir, 2: melee_dir, 3: smash4_dir}

## Set the Rating Period Length to Two Weeks
rp_length = 2

## How many two week spans would it take for a player to become completely uncertain?
#      Probably 3 years. So 26*3 = 78 Rating Periods

rp_decay = 78
average_rd = 75

#From the glicko formula
c_val = sqrt(((350**2) - average_rd**2) / (rp_decay**2))

tournaments = []
all_players = keydefaultdict(Player)
all_matches = []

game = raw_input("What game would you like to generate glicko for? \n1: 64 \n2: Melee \n3: Smash4\n")


#Get tournaments in sorted order.
first = 1
with open('../data/' + game_dirs[int(game)] + '/Singles/tournaments.csv') as stream:
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

sorted_tourneys = tnmt_array[tnmt_array[:,1].argsort()]



iteration = 0
prev_rp = -1
for tourney in sorted_tourneys:
    current_matches = []
    current_players = np.array([])
    with open('../data/' + game_dirs[int(game)] + '/Singles/' + tourney[0] + '-sets.csv') as stream:
        try:
            has_header = csv.Sniffer().has_header(stream.read(1024))
        except:
            print(tourney)
            exit(-1)
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

            #Create the player and add it to the current tournament, incrementing their set count.
            current_players = np.append(current_players, all_players[set_data[0]])
            current_players = np.append(current_players, all_players[set_data[1]])

            #Check if the set was a DQ
            if(int(set_data[3]) == -1 or int(set_data[4] == -1)):
                continue

            #Update the number of sets and win/loss
            all_players[set_data[0]].num_sets += 1
            all_players[set_data[1]].num_sets += 1
            if(not int(set_data[2])):
                all_players[set_data[0]].wlr[0] += 1
                all_players[set_data[1]].wlr[1] += 1
            else:
                all_players[set_data[0]].wlr[1] += 1
                all_players[set_data[1]].wlr[0] += 1

            current_matches.append(Match([all_players[set_data[0]], all_players[set_data[1]]], int(set_data[2])))

        #Figure out the current rating period and set each player's last rating period accordingly.
        current_rp = (datetime.datetime.strptime(tourney[1], "%Y-%m-%d") - datetime.datetime(2016, 1, 1)).days/14
        current_players = np.unique(current_players)
        for player in current_players:
            player.num_tournaments += 1
            if player.last_rp == -1:
                player.last_rp = current_rp

        #If we're in a new rating period, or we're the last tournament, then update the ratings
        if(prev_rp != current_rp or tourney[0] == sorted_tourneys[len(sorted_tourneys) - 1][0]):
            rp_tournaments = Tournament(current_players, current_matches, c_val)
            rp_tournaments.update_ratings(current_rp)
        prev_rp = current_rp
        iteration += 1
    

#Take care of decay with respect to the current rating period.
first = 1
for player in all_players:
    all_players[player].decay_RD(26, c_val)
    if first:
        first = 0
        rankings = np.array([all_players[player].name, all_players[player].rating, all_players[player].RD, all_players[player].num_sets, all_players[player].wlr[0], all_players[player].wlr[1], all_players[player].num_tournaments ])
        rankings.shape = (1,7)
    rankings = np.append(rankings, np.array([all_players[player].name, all_players[player].rating, all_players[player].RD, all_players[player].num_sets, all_players[player].wlr[0], all_players[player].wlr[1], all_players[player].num_tournaments ]).reshape(1,7),axis=0)


final = rankings[rankings[:,1].argsort()[::-1]]
f = open(game_dirs[int(game)] + "SinglesGlicko.csv", 'w')
f.write("player,rating,rd,sets,wins,losses,num_tourneys\n")
for pl in final:
    f.write(",".join(pl) + '\n')

f.close()

