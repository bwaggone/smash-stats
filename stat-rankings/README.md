# Stat Calculators Readme

Currently I have two calculators included with this program, a custom implemented **Glicko** calculator, and an implementation of Microsoft's **TrueSkill** algorithm. Both have their pros and cons, and I recommend you check out the data guarantees on the main page's readme before deciding to use either. Here are the instructions to use,

##TrueSkill
After installing the dependencies, run,
```
python TrueSkillCalc.py
```
You will see the following prompt,
```
What game would you like to generate TrueSkill Rankings for?
1. 64
2. Melee
3. Smash4
```
Type the desired option (1, 2, or 3), and wait. There is currently no feedback on when the operation is finished, just check when you gain control of the console again. The output will be in the following file, [game]SinglesTrueSkill.csv.

##Glicko
Once dependencies are installed, runm
```
python GlickoCalc.py
```
You will see the following prompt,
```
What game would you like to generate Glicko Rankings for?
1. 64
2. Melee
3. Smash4
```
Type the desired option (1, 2, or 3), and wait. There is currently no feedback on when the operation is finished, just check when you gain control of the console again. The output will be in the following file, [game]SinglesGlicko.csv.

#Glicko Implementation Details

## Mathematical Background
There are resources online and much more eloquent speakers than me than can explain this part to you. The bulk of the resources I used were from the following two sources,

https://en.wikipedia.org/wiki/Glicko_rating_system
http://www.glicko.net/glicko/glicko.pdf
http://www.glicko.net/glicko/glicko2.pdf

**This calculator is an implementation of the original Glicko rating system, Glicko-2 is a battle for another day**.

## Classes and Objects

As written, I have three major objects used within the calculator, which all work in conjunction with one another. There is the **Player** class, **Match** and **Tournament** classes.

### Player
A player contains data to help formulate the Glicko Rating easily. It contains the following functions:
```python
class Player:
  self.rating; self.RD; self.g_RD; self.last_rp
  self.name
  self.wlr[2]; self.num_sets; self.num_tournaments
  def __init__(self, name):
  def update_g_RD(self):
  def decay_RD(self, rp, c):
```
Its default constructor requires a name, and will set the glicko rating and RD to 1500/350 respectively. It also keeps track of the last rating period the player competeted in, set to -1 if never competed. **If RD is ever changed, recalculate g_RD using the built in method (self.update_g_RD()). If this is not done, glicko will be calculated incorrectly.** Players will not decay their RD unless the method is called per player (which tournament handles in a few functions to be specified later). It takes in the current rating period, and the decay constant. It will ~~not~~ work if rp passed in is earlier than the last rating period the player played in, so use with caution.

### Match
A match contains the two players, and the outcome of said match. It does not include any specific game counts, just if a player won, or lost. It also makes no distinction about byes or DQs, so **it is the responsibility of the programmer to filter out DQs**.
```python
class Match:
  self._players[2]
  self._win_loss;
  self.expect_s[2]
  def __init__(self, players, win_loss):
```
Not much to see here. Players is a list of two Player Objects above. win_loss is 0 if \_players[0] won and 1 otherwise. expect\_s is a helper variable used for glicko calculation. It's a long expected value term that roughly translated to the expected outcome of the match, but not exactly. Don't rely on expect\_s to predict outcomes. It is a list of two floats.

### Tournament
Tournament is a bit of a misnomer, but until I find a suitable replacement word, tournament will stand. A Tournament object contains all the players, and matches of a single rating period. It contains a few helper member variables for glicko computation.

```python
class Tournament:
    self._matches; self._players; self.c;
    self._rupdateConst #defaultdict(float)
    self._d2s #defaultdict(float)
    self._setsthistournament #defaultdict(int)
    def __init__(self, players, matches, c):
    def update_ratings(self, rp):
        def calc_decay(self, rp):
        def calc_d_sqrd(self):
```

This is where the fun math is. Matches/Players are both lists, and every other variable is used in calculation of glicko stats. I attempted to name the variables similarly to their mathematical counterparts, and to keep track of every player's calculation, I needed a few dictionaries. update\_ratings will alter every player's rating, RD, g_RD, and last_rp according to the results of the matches in the current rating period. It will also account for skill decay between tournaments, and as such needs the decay constant c passed into the constructor. **If you would like to run the calculator with no skill decay, pass 0 in for c**. *It might be prudent to move the helper variables inside of update_ratings...
