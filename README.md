##A Project Intended to Aggregate Glicko Statistics for Smash Bros. Players.
###Version: 0.0.3

Below is a general list of tasks to get done, stretch goals, and what has actually been accomplished. I don't think this is really ready for an official release yet, but it is *usable*. Barely.

####DONE
* Glicko Calculator
* Smash.gg API Scraper
* Data file structure
* Have master tournament files with a list of slugs + dates + entrants
* 64/Melee/Brawl/PM/Smash4 Support (Scraping)
* Define glicko rating periods, add RD Decay
* Modify master tournament file to scrape entrant numbers

####TO-DO
* Add support for more than one Calendar year + tournament timeout
* Create and update a list of tournament slugs to scrape from
* ~~Reorganize file structure for the scraper code~~, give a blank set of slugs to scrape from
* Pipe data results to Glicko/Custom calculator. \**partially done*
* Add exceptions to calculator, ignore results from player X on tournament Y.
* **Clean the glicko calculator code holy shit it looks like a nightmare**

####KNOWN ISSUES
* People with pipes (|) in their tag. *Currently no way to distinguish a pipe and a sponsor separator without bombarding smash.gg with a billion API requests*. This is not an issue for doubles files, only singles.
* Does **not** work on tournaments that run games other than smash. (Rivals of Aether, other fighting games).
* **EVO is excluded because it is not hosted on smash.gg. It will have to be added manually to the data, or another method needs to be used. **
*  Consistency between names needs to be manually fixed. Ex: Some tournaments list mang0 as mango, and superboomfan as superboom. The goal is to maintain a "fix" file to run and check all applicable files for the player.

####Future Goals:
* ~~Scrape the smash.gg api to get tournament results~~
* Make the glicko calculator standalone (maybe a python package?)
* ~~Output the results to a csv~~
* Add a predictor for a head to head given current Glicko ratings
* Use the predictor to model the likelihood of player X winning tournament Y

### Data Guarantees and Glicko
Most of the information I've gathered about glicko has come from both wikipedia, and a pdf [from glicko himself.](http://www.glicko.net/glicko/glicko.pdf) The glicko system can be **VERY** volatile. Players who don't compete very often but have a high skill tend to have their rankings change more drastically than their peers who compete more often. Therefore, a player's rating is more likely to change if they're new, or haven't competed in awhile. This does lead to some anomolies with rankings and scores, but remember, glicko is intended to be interpreted as a **range** of possible skill values, not a true skill value.

For example, if we have a player who's rating is 1800 and they have a rating deviation of 67, we are 95% confident that their true rating is between 1800 +/- (2\*67).

Based on how the data is gathered, it's easy for data to be missed or attributed incorrectly. Cases where a player is known by more than one name, typo'd in tournament, or two players have the same name can skew this data (albiet not by much unless you're a certain smash4 player who thinks it's cool to change your tag every other month). In an ideal world, if everyone had roughly the same amount of matches, these rankings would be more representative, but hey, that's what statistics is supposed to tell you anyway. Take the ratings with a grain of salt, and I'll eventually try to find ways to lower the variance or provide multiple views on the data.
