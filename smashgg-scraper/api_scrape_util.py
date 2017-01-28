import time
import requests
import json
from collections import *


smash_games = defaultdict(str, {1: "Melee", 2: "ProjectM", 3: "Smash4", 4: "64", 5: "Brawl", 6: "YOLO"})
smash_formats = defaultdict(str, {1: "Singles", 2: "Doubles", 5: "Crews"})
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
