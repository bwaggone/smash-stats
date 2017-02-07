from util import *
from trueskill.backends import cdf
from math import sqrt


def win_prob(r1, r2):
    delta = r1.mu - r2.mu
    #Perhaps we should weight the uncertainty higher...
    rsss = sqrt(r1.sigma**2 + r2.sigma**2)
    return cdf(delta/rsss)

all_players = keydefaultdict(Player)

with open('MeleeSinglesTrueSkill.csv') as stream:
    has_header = csv.Sniffer().has_header(stream.read(1024))
    stream.seek(0)  # rewind
    incsv = csv.reader(stream)
    if has_header:
        next(incsv)  # skip header row

    for ranking_data in incsv:
        all_players[ranking_data[0]].rating = Rating(float(ranking_data[1]), float(ranking_data[2]))


print(win_prob(all_players["duck"].rating, all_players["pewpewu"].rating))
