import os
import fileinput
import sys

fix_file = open('name_fixes.csv', 'r')

labels = fix_file.readline()

for line in fix_file:
    fix_info = line.replace('\n', '').split(',')
    print(fix_info)
    #Open the tournament file associated with the game
    tourneys_filename = './' + fix_info[1] + '/Singles/tournaments.csv'
    tourneys_file = open(tourneys_filename, 'r')
    for line in tourneys_file:
        tourney_info = line.replace('\n', '').split(',')
        if(tourney_info[0] == 'Tournament'):
            continue
        for line in fileinput.input(['./' + fix_info[1] + '/Singles/' + tourney_info[0] + '-standings.csv'], inplace = 1):
            sys.stdout.write(line.replace(fix_info[0] + ',', fix_info[2] + ','))
        for line in fileinput.input(['./' + fix_info[1] + '/Singles/' + tourney_info[0] + '-sets.csv'], inplace = 1):
            sys.stdout.write(line.replace(fix_info[0] + ',', fix_info[2] + ','))
