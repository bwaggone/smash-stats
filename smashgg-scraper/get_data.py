import requests
import csv
import time
import json
from collections import *
from api_scrape_util import *
import threading
import sys

def get_data(slug, supress_output):
    tourn_info = get_tournament_info(slug)
    event_phases = tourn_info['phases_per_event']
    phase_groups = tourn_info['groups_per_phase']

    #Separate each phase by game
    events = {}
    for event_id in event_phases:
        r = requests.get(format_url(api_prefix, 'event/', str(event_id), api_entrant_postfix))
        evnt_data = json.loads(r.text)
        events[evnt_data["entities"]["event"]["id"]] = Event(event_id, evnt_data["entities"]["event"]["name"], evnt_data["entities"]["event"]["videogameId"], evnt_data["entities"]["event"]["type"])
        tmp = evnt_data["entities"]["entrants"]
        events[evnt_data["entities"]["event"]["id"]].add_entrants(tmp)

    #At this point, we've scrapped all events, phases, and entrants
    #print("Retrieved events")

    for event in events:
        events[event].add_phases(event_phases[event])
        for phase in events[event].phases:
            events[event].add_groups(phase_groups[phase])
       
    for event in events:
        #Uses the skip criteria defined in skip_event to check if we care about this event.

        if(skip_event(events, event)):
            continue
        
        #Update the master tournament file
        master_file = "../data/" + events[event].game + "/" + events[event].format + "/tournaments.csv" 

        master_lock.acquire()
        update_master_file(master_file,slug, tourn_info['name'], tourn_info['dates'], events[event])
        master_lock.release()

        
        #Update the sets file
        filename = get_filename(events[event].game, events[event].format,slug,'-sets.csv')
        if(not supress_output):
            print("Working on " + filename + "...")
        doubles = write_set_data(filename, events[event], supress_output)


        
        #Update the standings file
        filename = get_filename(events[event].game, events[event].format,slug,'-standings.csv')
        write_placements(filename, events[event], doubles)

    if(supress_output):
        slug_lock.acquire()
        all_slugs.pop(slug, None)
        slug_lock.release()


#Declare all needed threads and locks
threads = []
all_slugs = {}
master_lock = threading.RLock()
slug_lock = threading.RLock()

def Single():
    slug = raw_input("What is the tournament slug?\n")
    get_data(slug, False)


def Multi():
    #Open the slugs file to read all tournaments to scrape
    slug_file = "../data/slugs.csv"
    f = open(slug_file,"r")
    reader = csv.reader(f)
    slug_list = list(reader)
    iterations = len(slug_list[1::])

    for i in range(1,iterations + 1):
        slug = slug_list[i][1]
        slug_lock.acquire()
        all_slugs[slug] = slug
        #print("Starting Tournament: ", slug)
        slug_lock.release()
        #Create a thread to grab data, surpress output
        t = threading.Thread(target=get_data, args=(slug,True))
        threads.append(t)
        t.start()

    #Print the remaining threads, and check every half second.
    while(threading.activeCount() != 1):
        sys.stdout.write("Threads Remaining: {0}\r".format(threading.activeCount()))
        sys.stdout.flush()
        time.sleep(0.5)

    for thread in threads:
        thread.join()

    print("Error'd files: ", all_slugs)


mode = raw_input("Single Mode (s)? Or File Mode (f)?\n")

valid = False
if(mode == "s"):
    Single()
    valid = True
if(mode == "f"):
    Multi()
    valid = True
if(not valid):
    print("Please select a valid mode and rerun.")
