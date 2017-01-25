import requests
import sys
import time
import json
from collections import *
from api_scrape_util import *
import threading
import csv
import progressbar

threads = []
all_slugs = {}
lock = threading.RLock()
slug_lock = threading.RLock()

def tourn_scraper(slug):
    r = requests.get('https://api.smash.gg/tournament/' + slug + '?expand[]=phase&expand[]=groups&expand[]=event')
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

    #print("Retrieved events")

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

        #Corner Cases: Lane Shift - Shine 2016
        #              Character Crews - Pound 2016
        #              Low Tiers: Multiple events
        #              YOLO - Smash 64 in general
        #              Big Brother Teams - Eden


        if(not_found or events[event].game == "YOLO" or events[event].game == "" or events[event].format == "Crews" or ("Lane Shift" in events[event].event_name) or ("Crews" in events[event].event_name) or ("Low Tier" in events[event].event_name) or ("Teams" in events[event].event_name)):
            #print("Skipping 1 event")
            continue
        
        master_file = "../data/" + events[event].game + "/" + events[event].format + "/tournaments.csv" 
        lock.acquire()
        try:
            master = open(master_file)
            master.close()
            check = False
            with open(master_file, "r") as master:
                for line in master:
                    if slug in line:
                        check = True

            if(not check):
                master = open(master_file, "a")
                master.write(slug + "," + tournament_dates[0] + "," + tournament_dates[1] + "," + str(len(events[event].entrants)) + "\n")
                master.close()
        except:
            master = open(master_file, "a+")
            master.write("Tournament,startDate,endDate,entrants\n")
            master.write(slug + "," + tournament_dates[0] + "," + tournament_dates[1] + "," + str(len(events[event].entrants)) + "\n")
            master.close()

        lock.release()
        filename = "../data/" + events[event].game + "/" + events[event].format + "/" + slug + "-sets.csv" 
        # print("Working on " + filename + "...")


        #####PROGRESS BAR CODE ##########
        # num_of_groups = 0
        # bar = progressbar.ProgressBar(maxval=len(events[event].groups),widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        # bar.start()
        #################################
        
        f = open(filename, "w")
        if(events[event].format == "Doubles"):
            doubles = 1
            f.write("T1P1,T1P2,T2P1,P2P2,set winner,T1Score,T2Score\n")
        else:
            doubles = 0
            f.write("P1,P2,set winner,P1Score,P2Score\n")
        
        for group in events[event].groups:
            # num_of_groups += 1
            # bar.update(num_of_groups)

            results = requests.get(api_prefix + 'phase_group/' +  str(group) + api_sets_postfix)
            result_data = json.loads(results.text)
            #print("Retrieving sets from group #:" + str(group))

            if(result_data["entities"]["groups"]["hasSets"] == False):
                continue
            
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

        # bar.finish()
        # print("Wrote Results to " + filename)
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
    slug_lock.acquire()
    # print("Finished " + slug)
    all_slugs.pop(slug, None)
    slug_lock.release()


slug_file = "../data/slugs.csv"
f = open(slug_file,"r")
reader = csv.reader(f)
slug_list = list(reader)
iterations = len(slug_list[1::])
for i in range(1,iterations):
    slug = slug_list[i][1]
    slug_lock.acquire()
    all_slugs[slug] = slug
    slug_lock.release()
    t = threading.Thread(target=tourn_scraper, args=(slug,))
    threads.append(t)
    t.start()

while(threading.activeCount() != 1):
    sys.stdout.write("Threads Remaining: {0}\r".format(threading.activeCount()))
    sys.stdout.flush()
    time.sleep(0.5)

for thread in threads:
    # print("Threads Remaining: {0}\r".format(threading.activeCount(),))
    thread.join()

# slug_list = ["pound-2016", "shine-2016"]

# for i in range(0,2):
    # print("Redoing Failed Tournament: " + slug_list[i])
    # tourn_scraper(slug_list[i]);

print(all_slugs)
