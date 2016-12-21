##A Project Intended to Aggregate Glicko Statistics for Smash Bros. Players.
###Version: 0.0.1

Below is a general list of tasks to get done, stretch goals, and what has actually been accomplished. I don't think this is really ready for an official release yet, but once I feel like I'm at V: 0.1.0, I'll share it with the smash community via reddit/facebook/smashboards.

####DONE
* Glicko Calculator
* Smash.gg API Scraper
* Data file structure
* Have master tournament files with a list of slugs + dates + entrants
* 64/Melee/Brawl/PM/Smash4 Support (Scraping)

####TO-DO
* Define glicko rating periods, add RD Decay + tournament timeout
* Create and update a list of tournament slugs to scrape from
* Modify master tournament file to scrape entrant numbers
* Reorganize file structure for the scraper code, give a blank set of slugs to scrape from
* Pipe data results to Glicko/Custom calculator. \**partially done*
* Add exceptions to calculator, ignore results from player X on tournament Y.

####KNOWN ISSUES
* People with pipes (|) in their tag. *Currently no way to distinguish a pipe and a sponsor separator without bombarding smash.gg with a billion API requests*. This is not an issue for doubles files, only singles.
* Does **not** work on tournaments that run games other than smash. (Rivals of Aether, other fighting games).
* **EVO is excluded because it is not hosted on smash.gg. It will have to be added manually to the data, or another method needs to be used. **
*  Check into superboom vs. superboomfan for GOML, the lack of consistency is worrying.

####Future Goals:
* ~~Scrape the smash.gg api to get tournament results~~
* Make the glicko calculator standalone (maybe a python package?)
* ~~Output the results to a csv~~
* Add a predictor for a head to head given current Glicko ratings
* Use the predictor to model the likelihood of player X winning tournament Y
