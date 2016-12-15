from glicko import *


def run_summit_3():
    players = defaultdict(Player)
    player_names = ["Mango", "Mafia", "Westballz", "Shroomed", "Mew2King", "S2J", "Leffen",
                    "PewPewU", "Armada", "n0ne", "Plup", "Axe", "Hungrybox", "The Moon",
                    "SFAT", "Duck"]
    for player in player_names:
            players[player].name = player


    duck_games = {"SFAT": True, "Hungrybox": False, "Westballz": True, "Plup": False}
    players["Duck"].rating = 1500.0
    players["Duck"].RD = 200.0
    players["Duck"].update_g_RD()
    players["SFAT"].rating = 1550.0
    players["SFAT"].RD = 100.0
    players["SFAT"].update_g_RD()
    players["Hungrybox"].rating = 1700.0
    players["Hungrybox"].RD = 300.0
    players["Hungrybox"].update_g_RD()
    players["Westballz"].rating = 1400.0
    players["Westballz"].RD = 30.0
    players["Westballz"].update_g_RD()
    match_1 = Match([players["Duck"], players["Westballz"]], 0)
    match_2 = Match([players["Duck"], players["SFAT"]], 1)
    match_3 = Match([players["Duck"], players["Hungrybox"]], 1)
    summit = Tournament([players["Duck"], players["Hungrybox"], players["Westballz"], players["SFAT"]], [match_1, match_2, match_3])
    summit.update_ratings()
    print(players["Duck"].rating)



run_summit_3()
