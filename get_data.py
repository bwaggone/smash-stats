import requests
import json
from collections import *

api_prefix = 'https://api.smash.gg/'

smash_games = {1: "Melee", 3: "Smash 4"}

r = requests.get('https://api.smash.gg/tournament/the-big-house-6?expand[]=phase&expand[]=groups&expand[]=event')
#r = requests.get('https://api.smash.gg/phase_group/76016?expand[]=sets&expand[]=standings&expand[]=selections')
data = json.loads(r.text)
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




print(phase_groups)
#for event in data["entities"]["phase"]:
#    r = requests.get(api_prefix + 'event/' + str(event["eventId"]))
#    evnt_data = json.loads(r.text)
#    if(evnt_data["entities"]["event"]["name"] == "Melee Singles"):
#        print(evnt_data["entities"]["event"]["id"])
   # print(evnt_data["entities"]["event"]["name"])
