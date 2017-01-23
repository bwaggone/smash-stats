import requests
import time
import json
from collections import *
from api_scrape_util import *
import progressbar

slug = raw_input("What is the tournament slug?\n")

#r = requests.get('https://api.smash.gg/tournament/the-big-house-6?expand[]=phase&expand[]=groups&expand[]=event')
r = requests.get('https://api.smash.gg/tournament/' + slug + '?expand[]=phase&expand[]=groups&expand[]=event')
#r = requests.get('https://api.smash.gg/phase_group/76016?expand[]=sets&expand[]=standings&expand[]=selections')
data = json.loads(r.text)

tournament_dates = [time.strftime('%Y-%m-%d', time.localtime(data["entities"]["tournament"]["startAt"])),time.strftime('%Y-%m-%d', time.localtime(data["entities"]["tournament"]["endAt"]))]

phase_ids = []
event_ids = []
event_phases = defaultdict(list)
phase_groups = defaultdict(list)

#Get all event IDs
#Get all the phase IDs
#Assign each phase to its event
for phase in data["entities"]["phase"]:
    event_phases[phase["eventId"]].append(phase["id"])
    phase_ids.append(phase["id"])

#Assign each group to its phase.
for group in data["entities"]["groups"]:
    phase_groups[group["phaseId"]].append(group["id"])

#Separate each phase by game
events = {}
for event_id in event_phases:
    r = requests.get(api_prefix + 'event/' + str(event_id) + api_entrant_postfix)
    evnt_data = json.loads(r.text)
    events[evnt_data["entities"]["event"]["id"]] = Event(event_id, evnt_data["entities"]["event"]["name"], evnt_data["entities"]["event"]["videogameId"], evnt_data["entities"]["event"]["type"])
    tmp = evnt_data["entities"]["entrants"]
    events[evnt_data["entities"]["event"]["id"]].add_entrants(tmp)

print("Retrieved events")

for event in events:
    events[event].add_phases(event_phases[event])
    for phase in events[event].phases:
        events[event].add_groups(phase_groups[phase])
   
for event in events:
    #This prevents side events from being recorded
    # Ex: Own the House in TBH6
    not_found = 1
    for format_num in smash_formats:
        if(smash_formats[format_num] in events[event].event_name):
            not_found = 0
            break;
   
    #64, why do you have a "game" called YOLO? pls
    if(not_found or events[event].game == "YOLO" or events[event].game == ""):
        print("Skipping 1 event")
        continue
    
    master_file = "../data/" + events[event].game + "/" + events[event].format + "/tournaments.csv" 
    try:
        master = open(master_file)
        master.close()
        master = open(master_file, "a")
        master.write(slug + "," + tournament_dates[0] + "," + tournament_dates[1] + "," + str(len(events[event].entrants)) + "\n")
        master.close()
    except:
        master = open(master_file, "a+")
        master.write("Tournament,startDate,endDate,entrants\n")
        master.write(slug + "," + tournament_dates[0] + "," + tournament_dates[1] + "," + str(len(events[event].entrants)) + "\n")
        master.close()
    
    filename = "../data/" + events[event].game + "/" + events[event].format + "/" + slug + "-sets.csv" 
    print("Working on " + filename + "...")


    #####PROGRESS BAR CODE ##########
    num_of_groups = 0
    bar = progressbar.ProgressBar(maxval=len(events[event].groups),widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    #################################
    
    f = open(filename, "w")
    if(events[event].format == "Doubles"):
        doubles = 1
        f.write("T1P1,T1P2,T2P1,P2P2,set winner,T1Score,T2Score\n")
    else:
        doubles = 0
        f.write("P1,P2,set winner,P1Score,P2Score\n")
    
    for group in events[event].groups:
        num_of_groups += 1
        bar.update(num_of_groups)

        results = requests.get(api_prefix + 'phase_group/' +  str(group) + api_sets_postfix)
        result_data = json.loads(results.text)
        #print("Retrieving sets from group #:" + str(group))
        for _set in result_data["entities"]["sets"]:
            p1 = _set["entrant1Id"]
            p2 = _set["entrant2Id"]
            p1_score = _set["entrant1Score"]
            p2_score = _set["entrant2Score"]

            if(p1_score == None):
                p1_score = -2
            if(p2_score == None):
                p2_score = -2

            if(p1 == None or p2 == None):
                continue
            result = 0
            if _set["winnerId"] == p2:
                result = 1

            try:
                f.write(events[event].entrants[p1] + ',' + events[event].entrants[p2] + ',' + str(result) + "," + str(p1_score) + "," + str(p2_score) + '\n')
            except:
                f.write((events[event].entrants[p1] + ',' + events[event].entrants[p2] + ',' + str(result) + "," + str(p1_score) + "," + str(p2_score) +'\n').encode('utf-8'))

    bar.finish()
    #print("Wrote Results to " + filename)
    f.close()

    filename = "../data/" + events[event].game + "/" + events[event].format + "/" + slug + "-standings.csv" 
    f = open(filename, "w")
    if(events[event].format == "Doubles"):
        f.write("p1,p2,finalPlacement\n")
    else:
        f.write("name,finalPlacement\n")
    
    for placing in events[event].placings:
        try:
            f.write(split_doubles_names(events[event].entrants[placing], doubles) + "," + str(events[event].placings[placing]) + "\n")
        except:
            f.write((split_doubles_names(events[event].entrants[placing], doubles) + "," + str(events[event].placings[placing]) + "\n").encode('utf-8'))
    f.close()


#At this point we have every event with all group numbers, so we can use each one to look up set information.
#Once we have set information, we can output to csv (after translating entrantId -> name)




#   Get the game / event via request
#   r = requests.get(api_prefix + 'event/' + str(event_phases.key))
#   Save the game name, type, phase ids and groups to one object

#   Event Contains:
#       Several Phases
#       Phase Contains:
#           Several Groups
#           Group Contains:
#               Sets
#               Set contains:
#                   Players
#                   Winner


#======
#=TODO=
#======
#Create a class for event
#Create a class for phase
#Create a class for group
#Create a class of set
#Create a lookup table from entrantID to player name

#After we get the results, spit them out into a csv
#Read the CSV into the glicko calc

