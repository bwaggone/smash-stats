import os
import fileinput
import sys

# Create dict of names that need to be replaced
name_map = {}  # maps obsolete playertag to new, desired playertag
game_map = {}  # maps player tag to game that player plays.
with open('name_fixes.csv', 'r') as names_input:
    for line in names_input:
        if "name,game,to" in line:  # skip header line
            continue
        parts = line.strip().split(',')
        name_map[parts[0]] = parts[2]
        game_map[parts[0]] = parts[1]

# Run through every game type folder
for game_type in ["64","Melee","ProjectM","Brawl","Smash4"]:
    # Run through every file in dir with suffix -standings.csv
    for filename in os.listdir("./" + game_type + "/Singles/"):
        if not (filename.endswith("-standings.csv") or filename.endswith("-sets.csv")):
            continue

        for line in fileinput.input(['./' + game_type + '/Singles/' + filename], inplace = 1):
            parts = line.strip().split(',')
            for j in [0,1]:  # for player 1 and 2 in the match,
                if parts[j] in name_map.keys():  # if playertag in the name_map, change it
                    if parts[j] in game_map.keys():  # first check we're in the right game
                        if game_map[parts[j]] == game_type:
                            parts[j] = name_map[parts[j]]

            newline = parts[0]
            for part in parts[1::]:
                newline += ',' + part
            sys.stdout.write(newline + '\n')
