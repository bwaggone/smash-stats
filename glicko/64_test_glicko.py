from glicko import *
import time
import datetime
import collections
import csv
import os
import numpy as np

sixtyfour_dir = '../data/64/Singles/'

## Set the Rating Period Length to Two Weeks
rp_length = 2

## How many two week spans would it take for a player to become completely uncertain?
#      Probably 3 years. So 26*3 = 78 Rating Periods

rp_decay = 78
average_rd = 75
c_val = sqrt(((350**2) - average_rd**2) / (rp_decay**2))

#files = (os.listdir(os.getcwd() + '/../data/64/Singles/'))
tournaments = []
all_players = keydefaultdict(Player)
all_matches = []

#for f in files:
#    if 'sets' in f:
#        tournaments.append(f)

#f = open(sixtyfour_dir + 'tournaments.csv', 'r')
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
#Get tournaments in sorted order.
sorted_tourneys = tnmt_array[tnmt_array[:,1].argsort()]


#prev_rp = ((datetime.datetime.strptime(sorted_tourneys[0][1], "%Y-%m-%d") - datetime.datetime(2016, 1, 1)).days) / 14
#current_rp = prev_rp
prev_rp = -1
for tourney in sorted_tourneys:
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

            #Create the player and add it to the current tournament, incrementing their set count.
            current_players = np.append(current_players, all_players[set_data[0]])
            current_players = np.append(current_players, all_players[set_data[1]])

            #Check if the set was a bye
            if(int(set_data[3]) == -1 or int(set_data[4] == -1)):
                continue

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
            if player.last_rp == -1:
                player.last_rp = current_rp
        if(prev_rp != current_rp or tourney == sorted_tourneys[len(sorted_tourneys - 1)]):
            rp_tournaments = Tournament(current_players, current_matches, c_val)
            rp_tournaments.update_ratings(current_rp)
        prev_rp = current_rp
    
first = 1
for player in all_players:
    all_players[player].decay_RD(26, c_val)
    if first:
        first = 0
        rankings = np.array([all_players[player].name, all_players[player].rating, all_players[player].RD, all_players[player].num_sets, all_players[player].wlr[0], all_players[player].wlr[1] ])
        rankings.shape = (1,6)
    rankings = np.append(rankings, np.array([all_players[player].name, all_players[player].rating, all_players[player].RD, all_players[player].num_sets, all_players[player].wlr[0], all_players[player].wlr[1] ]).reshape(1,6),axis=0)


final = rankings[rankings[:,1].argsort()[::-1]]
f = open("64SinglesGlicko.csv", 'w')
f.write("player,rating,rd,sets,wins,losses\n")
for pl in final:
    f.write(",".join(pl) + '\n')

f.close()

'''
rating_period_test = Tournament(all_players, all_matches)
rating_period_test.update_ratings()
first = 1
for player in all_players:
    if first:
        first = 0
        test_array = np.array([all_players[player].name, all_players[player].rating, all_players[player].RD])
        test_array.shape = (1,3)#test_array.reshape((3,1))
#        print(test_array.shape)
    test_array = np.append(test_array, np.array([all_players[player].name, all_players[player].rating, all_players[player].RD]).reshape(1,3), axis = 0)

#print(test_array)

final = test_array[test_array[:,1].argsort()[::-1]]
f = open('test.out', "w")
for row in final:
    f.write(row[0] + ',' + str(row[1]) + ',' + str(row[2]) + '\n')


f.close()
matches = []'''
