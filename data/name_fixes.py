import os
import fileinput
import sys

def replaceAll(file_object,searchExp,replaceExp):
    for line in file_object
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

for line in fileinput.input(files, inplace = 1): 
          print line.replace("foo", "bar"),
          
fix_file = open('name_fixes.csv', 'r')

labels = fix_file.readline()

for line in fix_file:
    fix_info = line.replace('\n', '').split(',')
    #Open the tournament file associated with the game
    tourneys_filename = './' + fix_info[1] + '/Singles/tournaments.csv'
    tourneys_file = open(tourneys_filename, 'r')
    for line in tourneys_file:
        tourney_info = line.replace('\n', '').split(',')
        for line in fileinput.input(['get-on-my-level-2016-standings.csv'], inplace = 1):
            print line.replace("mango", "mang0")
