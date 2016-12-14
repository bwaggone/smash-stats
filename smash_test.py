from collections import *
from math import *

class Player:
    def __init__(self):
        q = log(10) / 400.0
        self.rating = 1500
        self.RD = 350
        self.name = "default"
        self.g_RD = 1 / sqrt(1 + 3*q*q * self.RD**2 / (pi*pi)) 

    def update_g_RD(self):
        q = log(10) / 400.0
        self.g_RD = 1 / sqrt(1 + 3*q*q * self.RD**2 / (pi*pi)) 


class Match:
    def __init__(self, players, win_loss):
        #players are P1 and P2
        #win_loss = 0 if P1 wins
        self._players = players
        self._winner = win_loss
        self._win_loss = win_loss
        #Once we know the players, we can get the expected outcome.
        pt1 = ((self._players[1].g_RD)*((self._players[0].rating - self._players[1].rating)/-400.0)) 
        pt2 = ((self._players[0].g_RD)*((self._players[1].rating - self._players[0].rating)/-400.0)) 
        self.expect_s = [(1 /(1 + 10**(pt1))), (1 / (1 + 10**(pt2)))]

    def contribution(self):

        raise "Not Implemented"
        #Calculate the contribution of this match to a player's rating change.
        #Returns a tuple

class Tournament:
    def __init__(self, players, matches):
        self._matches = matches
        self._players = players
        #q = log(10) / 400
        self._d2s = defaultdict(float)
        self._rupdateConst = defaultdict(float)
        #d^2 = 1 / (q^2 + sum of all games[(g(RD_i))^2 * E(X) *  (1 - E(X)))

    def update_ratings(self):
        def calc_d_sqrd(self):
            #Set up the d^2 dictionary from string -> float
            player_d2 = defaultdict(float)
            player_r = defaultdict(float)
            q = log(10) / 400.0

            #For each match
            for i in range(0, len(self._matches)):
                #Get a shorthand for the player/match info
                match_info = self._matches[i]
                p1 = match_info._players[0]
                p2 = match_info._players[1]
                #Update the sum for the denominator of d^2
                player_d2[p1.name] += (p2.g_RD**2)*match_info.expect_s[0]*(1 - match_info.expect_s[0])
                player_d2[p2.name] += (p1.g_RD**2)*match_info.expect_s[1]*(1 - match_info.expect_s[1])

                #Update the sum for the constant used to update ranking of a player

                #match_info.win_loss is zero if p1 wins, one if p1 losses. For the formula we need the opposite
                player_r[p1.name] += (p2.g_RD)*(abs(1 - match_info._win_loss) - match_info.expect_s[0])
                player_r[p2.name] += (p1.g_RD)*(match_info._win_loss - match_info.expect_s[1])

            for player in self._players:
                player_d2[player.name] = 1/((q**2) * player_d2[player.name])

            self._d2s = player_d2
            self._rupdateConst = player_r
        
        calc_d_sqrd(self)
        
        q = log(10) / 400.0
        for player in self._players:
            new_rating = player.rating + (q / ( ( 1 / player.RD**2 ) + (1 / self._d2s[player.name]) ) ) * self._rupdateConst[player.name]
            new_RD = sqrt(( ( 1 / player.RD**2 ) + (1 / self._d2s[player.name]))**-1 )
            player.rating = new_rating
            player.RD = new_RD
            player.update_g_RD()
            #print(player.rating + (q / ( ( 1 / player.RD**2 ) + (1 / self._d2s[player.name]) ) ) * self._rupdateConst[player.name])
            #print(sqrt(( ( 1 / player.RD**2 ) + (1 / self._d2s[player.name]))**-1 ))



#    def calc_d_sqrd(self):
        #Set up the d^2 dictionary from string -> float
        #player_d2 = defaultdict(float)
        #player_r = defaultdict(float)
        #q = log(10) / 400.0

        #For each match
        #for i in range(0, len(self._matches)):
            #Get a shorthand for the player/match info
        #    match_info = self._matches[i]
        #    p1 = match_info._players[0]
        #    p2 = match_info._players[1]
            #Update the sum for the denominator of d^2
        #    player_d2[p1.name] += (p2.g_RD**2)*match_info.expect_s[0]*(1 - match_info.expect_s[0])
        #    player_d2[p2.name] += (p1.g_RD**2)*match_info.expect_s[1]*(1 - match_info.expect_s[1])

            #Update the sum for the constant used to update ranking of a player

            #match_info.win_loss is zero if p1 wins, one if p1 losses. For the formula we need the opposite
        #    player_r[p1.name] += (p2.g_RD)*(abs(1 - match_info._win_loss) - match_info.expect_s[0])
        #    player_r[p2.name] += (p1.g_RD)*(match_info._win_loss - match_info.expect_s[1])

        #for player in self._players:
        #    player_d2[player.name] = 1/((q**2) * player_d2[player.name])

        #self._d2s = player_d2
        #self._rupdateConst = player_r




def run_summit_3():
    players = defaultdict(Player)
    player_names = ["Mango", "Mafia", "Westballz", "Shroomed", "Mew2King", "S2J", "Leffen",
                    "PewPewU", "Armada", "n0ne", "Plup", "Axe", "Hungrybox", "The Moon",
                    "SFAT", "Duck"]
    for player in player_names:
            players[player].name = player
#            print(players[player].name)


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
    #print(players["SFAT"].g_RD, players["Duck"].g_RD)
    match_1 = Match([players["Duck"], players["Westballz"]], 0)
    match_2 = Match([players["Duck"], players["SFAT"]], 1)
    match_3 = Match([players["Duck"], players["Hungrybox"]], 1)
    #print(match_1.__dict__)
    #print(match_2.__dict__)
    #print(match_3.__dict__)
    summit = Tournament([players["Duck"], players["Hungrybox"], players["Westballz"], players["SFAT"]], [match_1, match_2, match_3])
    #summit.calc_d_sqrd()
    summit.update_ratings()
    print(players["Duck"].rating)



run_summit_3()

'''
The Glicko-2 System will rank players based on performance.
It involves an overall rating and a rating deviation. We say that we
are 95% sure that a player's true skill is at most 2*RD from the rating.

STEP 1:
	Determine a starting rating and RD (1500, 350).
	Choose a system constant, tau. (affects variability, usually between 0.3-1.2)
	Set a default volatility per player (0.06)

STEP 2 (GLICKO):

	Determine the new RD from the following formula:
	RD = min(sqrt((RD_0)^2 + c^2 * t), 350)
	Where c is a constant based on the skill uncertaintly over time
	and t is the time between the last rating (in rating periods)
	To solve for c, we would just say, "it takes 100 rating periods to reach
	maximum uncertainty, and average RD is 50" 350 = sqrt(50^2 + 100*c^2)


	After m games, determine a new ranking from the following equations:
	g(RD_i) = 1 / sqrt(1 + 3(q^2)*(RD_i^2) / (pi^2))
	E(X) = E(s | r, r_i, RD_i) = 1 / (1 + 10*(g(RD_i)(r-r_i) / (-400)))
	q = ln(10) / 400
	d^2 = 1 / (q^2 + sum of all games[(g(RD_i))^2 * E(X) *  (1 - E(X)))
	r = r_0 + (q / ((1 / RD^2) + (1 / d^2)))* sum of all games[g(RD_i) * (s - E(X))
	
	Where r_i is the rating of an opponent, s_i is the outcome of the individual game

STEP 2 (IF USING GLICKO-2):
	Convert from glicko to glicko-2
	mu = (rating - 1500)/173.7178
	phi = RD/173.7178
	volatility does not change.

	173.1718 is the scale factor, a constant.

STEP 3 (GLICKO-2):
	Compute the quantity v, the estimated variance of the player's
	reating based on game outcomes.

	g(phi) = 1/sqrt(1 + 3*phi*pi / (pi*pi))
	E(mu, mu_j, phi_j) = 1 / (1 + exp(-g(phi_j)(mu - mu_j)))

       v = (sum(g(phi_j)^2 * E(mu, mu_j, phi_j)(1 - E(mu, mu_j, phi_j))))^-1

STEP 4 (GLICKO-2):
	Compute Delta, the estimated improvement in rating

'''
