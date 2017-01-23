import mysql.connector
import numpy as np

cnx = mysql.connector.connect(user="root", password="lightning",host="127.0.0.1",database="smashstats")
cursor = cnx.cursor()


gamedirs = {'64': './64/Singles/', 'melee': './Melee/Singles/'}

def sanatize_name(name):
    return name.lower().strip()

add_tournament = ("INSERT INTO tourneys"
        "(name, site, game, entrants, startdate, enddate) "
        "VALUES (%s,%s,%s,%s,%s,%s)")

add_player = ("INSERT INTO players"
        "(tag, game)"
        "VALUES (%s, %s)")

add_set = ("INSERT INTO sets"
        "(p1tag, p2tag, p1id, p2id, winner, dq, p1games, p2games, tourneyid)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

tournaments = np.loadtxt(gamedirs['melee'] + 'tournaments.csv', dtype={'names': ['slug', 'date-start', 'date-end', 'entrants'], 'formats' : ['S64', 'S16', 'S16', 'i4']}, delimiter = ",", skiprows = 1, ndmin = 2)

count = 0
all_players = []
for tourney in tournaments:
    tourney_sets = gamedirs['melee']+ tourney['slug'][0] + '-sets.csv'
    tourney_standings = gamedirs['melee'] + tourney['slug'][0] + '-standings.csv'

    cursor.execute(add_tournament,(str(tourney['slug'][0]),"smash.gg", "melee", str(tourney['entrants'][0]),str(tourney['date-start'][0]),str(tourney['date-end'][0])))
    
    with open(tourney_standings, 'r') as f:
        for line in f:
            player_info = line.split(',')
            if(player_info[0] == 'name'):
                continue
            else:
                all_players.append(sanatize_name(player_info[0]))
                if("mango" in all_players):
                    print(tourney)
                    exit(-1)

unique_players = list(set(all_players))
player_to_id = {}
iteration = 0
for player in unique_players:
    player_to_id[str(player)] = iteration
    iteration += 1
    try:
        cursor.execute(add_player,((str(player),'melee')))
    except:
        print("Error with player" + str(player)) 
        #cursor.execute(add_player,(str(player).decode('utf-8').encode(),'melee'))
#print(unique_players)

iteration = 0
for tourney in tournaments:
    tourney_sets = gamedirs['melee']+ tourney['slug'][0] + '-sets.csv'
    iteration += 1
    print(tourney_sets)
    with open(tourney_sets, 'r') as f:
        for line in f:
            set_info = line.split(',')
            if(set_info[0] == "P1"):
                continue
            else:
                if(set_info[3] == -1 or set_info[4] == -1):
                    continue
                else:
                    try:
                        if(int(set_info[2]) == 0):
                            winner = int(player_to_id[str(set_info[0])])
                        else:
                            winner = int(player_to_id[str(set_info[1])])

                        cursor.execute(add_set,((str(set_info[0]), str(set_info[1]), player_to_id[str(set_info[0])], player_to_id[str(set_info[1])], winner, 0, int(set_info[3]), int(set_info[4]), iteration)))
                    except:
                        print("Error, set unreadable")


cnx.commit()

cnx.close()
