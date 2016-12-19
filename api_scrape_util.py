import time
import json
from collections import *


smash_games = {1: "Melee", 2: "ProjectM", 3: "Smash4", 4: "64", 5: "Brawl", 6: "YOLO"}
smash_formats = defaultdict(str, {1: "Singles", 2: "Doubles", 5: "Crews"})
api_prefix = 'https://api.smash.gg/'
api_entrant_postfix = '?expand[]=entrants'
api_sets_postfix = '?expand[]=sets'

#For the motherfuckers who have a pipe in their name.
#   DON'T YOU KNOW WE USE A PIPE FOR SPONSOR SHIT?!?
name_exceptions_type1 = ["TimKO | AF" , "Lv. 10 | AF"]

def sanatize_name(name):
    return (name.split('|', 1)[-1]).lower().replace('"', '').split('|', 1)[-1].lstrip()

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

class event:
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
                self.entrants[entrant["id"]] = sanatize_name(entrant["name"])
                self.placings[entrant["id"]] = entrant["finalPlacement"]
