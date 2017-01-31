import time
import requests
import json
from collections import *
import progressbar


#Constants defined by smash.gg's API
smash_games = defaultdict(str, {1: "Melee", 2: "ProjectM", 3: "Smash4", 4: "64", 5: "Brawl", 6: "YOLO"})
smash_formats = defaultdict(str, {1: "Singles", 2: "Doubles", 5: "Crews"})


#API Helpers
api_prefix = 'https://api.smash.gg/'
api_entrant_postfix = '?expand[]=entrants'
api_sets_postfix = '?expand[]=sets'
api_phase_postfix = '?expand[]=phase'
api_event_postfix = '?expand[]=event'


#Given the slug it will return in the following order:
#   Tournament Name (string)
#   Tournament Dates ([Date1, Date2])
#   A list of phases per event
#   A list of groups per phase

def get_tournament_info(slug):
    r = requests.get('https://api.smash.gg/tournament/' + slug + '?expand[]=phase&expand[]=groups&expand[]=event')
    data = json.loads(r.text)

    tournament_name = data["entities"]["tournament"]["name"]
    tournament_dates = [time.strftime('%Y-%m-%d', time.localtime(data["entities"]["tournament"]["startAt"])),time.strftime('%Y-%m-%d', time.localtime(data["entities"]["tournament"]["endAt"]))]
    
    phase_ids, event_ids = [], []

    event_phases, phase_groups = defaultdict(list), defaultdict(list)

    #Assign each phase to its event
    for phase in data["entities"]["phase"]:
        event_phases[phase["eventId"]].append(phase["id"])
        phase_ids.append(phase["id"])

    #Assign each group to its phase.
    for group in data["entities"]["groups"]:
        phase_groups[group["phaseId"]].append(group["id"])

    return {'name': tournament_name, 'dates': tournament_dates, 'phases_per_event': event_phases, 'groups_per_phase': phase_groups}

#This function will check if the event is worth recording, the following are criteria that if an event has, will be skipped:
#   Format is not 1 or 2 (Singles or Doubles)
#   Event Name Contains any of the following:
#       Lane Shift
#       Low Tier
#       Big Brother
#       Ladder
def skip_event(events, event):
    #This prevents side events from being recorded
    #   The check says, if the format is Singles/Doubles, but Singles/Doubles isn't in the title of the event, skip it
    not_found = 1
    for format_num in smash_formats:
        if(smash_formats[format_num] in events[event].event_name):
            not_found = 0
            break;
   
    if(not_found or events[event].game == "YOLO" or events[event].game == "" or events[event].format == "Crews" or ("Lane Shift" in events[event].event_name) or ("Crews" in events[event].event_name) or ("Low Tier" in events[event].event_name) or ("Big Brother" in events[event].event_name) or ("Ladder" in events[event].event_name)):
        return True

    return False



def update_master_file(master_filename, slug, tournament_name, tournament_dates, event):
    check = False
    try:
        #If we opened the file successfully, check if this tournament has already been recorded. If so, don't write to the master file.
        master = open(master_filename)
        master.close()
        with open(master_filename, "r") as master:
            for line in master:
                if slug in line:
                    check = True
                    break;

        if(not check):
            master = open(master_filename, "a")

    except Exception as inst:
        #If the file didn't exist, we'll create the master file.
        master = open(master_filename, "a+")
        master.write("Tournament,slug,startDate,endDate,entrants\n")

    if(not check):
        master.write(tournament_name + "," + slug + "," + tournament_dates[0] + "," + tournament_dates[1] + "," + str(len(event.entrants)) + "\n")
        master.close()

def format_url(prefix, req_type, type_id, postfix):
    return prefix + req_type + type_id + postfix

def get_filename(game, game_format, slug, set_or_standing):
    return "../data/" + game + "/" + game_format + "/" + slug + set_or_standing

def write_set_data(sets_file, event, supress):
    num_of_groups = 0
    if(not supress):
        bar = progressbar.ProgressBar(maxval=len(event.groups),widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

    f = open(sets_file, "w")
    if(event.format == "Doubles"):
        doubles = 1
        f.write("T1P1,T1P2,T2P1,P2P2,set winner,T1Score,T2Score\n")
    else:
        doubles = 0
        f.write("P1,P2,set winner,P1Score,P2Score\n")
    
    for group in event.groups:
        num_of_groups += 1
        if(not supress):
            bar.update(num_of_groups)

        results = requests.get(format_url(api_prefix, 'phase_group/', str(group), api_sets_postfix))
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

            #try:
            #    f.write(event.entrants[p1] + ',' + event.entrants[p2] + ',' + str(result) + "," + str(p1_score) + "," + str(p2_score) + '\n')
            #except:
            f.write((event.entrants[p1] + ',' + event.entrants[p2] + ',' + str(result) + "," + str(p1_score) + "," + str(p2_score) +'\n').encode('utf-8'))
    if(not supress):
        bar.finish()
    #print("Wrote Results to " + filename)
    f.close()
    return doubles


def write_placements(standings_file, event, doubles):
    f = open(standings_file, "w")
    if(doubles):
        f.write("p1,p2,finalPlacement\n")
    else:
        f.write("name,finalPlacement\n")
    
    for placing in event.placings:
    #    try:
    #        f.write(split_doubles_names(event.entrants[placing], doubles) + "," + str(event.placings[placing]) + "\n")
    #    except:
        f.write((split_doubles_names(event.entrants[placing], doubles) + "," + str(event.placings[placing]) + "\n").encode('utf-8'))

    f.close()



#For the motherfuckers who have a pipe in their name.
#   DON'T YOU KNOW WE USE A PIPE FOR SPONSOR SHIT?!?
name_exceptions_type1 = ["TimKO | AF" , "Lv. 10 | AF"]

def sanatize_name(name):
    return (name.split('|', 1)[-1]).lower().replace('"', '').split('|', 1)[-1].lstrip().replace(',','')

def sanatize_doubles(name):
    tmp = name.split('/')
    for i in range(0, len(tmp)):
        tmp[i] = tmp[i].lower().replace('"', '').strip()
    return ",".join(tmp)

def split_doubles_names(name, doubles):
    if(doubles):
        tmp = name.split('/')
        for i in range(0, len(tmp)):
            tmp[i] = sanatize_name(tmp[i].strip())
        return ",".join(tmp)
    else:
        return name

class Event:
    def __init__(self, event_id, event_name, gameId, _format):
        self.event_id = event_id
        self.event_name = event_name
        self.game = smash_games[gameId]
        self.format_id = _format
        self.format = smash_formats[_format]
        self.phases = []
        self.groups = []
        self.entrants = {}
        self.placings = {}

    def add_phases(self, phases):
        self.phases = phases

    def add_groups(self, groups):
        for group in groups:
            self.groups.append(group)


    def add_entrants(self, entrants):
        for entrant in entrants:
            if(self.format == "Doubles"):
                self.entrants[entrant["id"]] = sanatize_doubles(entrant["name"])
                self.placings[entrant["id"]] = entrant["finalPlacement"]
            else:
                #r = requests.get("https://api.smash.gg/entrant/" + str(entrant["id"]))
                #entrant_data = json.loads(r.text)
                #print(entrant_data["entities"]["attendee"][0]["gamerTag"])
                #self.entrants[entrant["id"]] = entrant_data["entities"]["attendee"][0]["gamerTag"]
                self.entrants[entrant["id"]] = sanatize_name(entrant["name"])
                self.placings[entrant["id"]] = entrant["finalPlacement"]
