##A Project Intended to Aggregate Glicko Statistics for Smash Bros. Players.

####DONE
* Glicko Calculator
* Smash.gg API Scraper
* Data file structure
* Have master tournament files with a list of slugs + dates
* 64/Melee/Brawl/Smash4 Support (Scraping)

####TO-DO
* Define glicko rating periods, add RD Decay + tournament timeout
* Create a list of tournament slugs to scrape from
* Modify master tournament file to scrape entrant numbers
* PM Support (Scraping)

####KNOWN ISSUES
* People with pipes (|) in their tag. *Currently no way to distinguish a pipe and a sponsor separator without bombarding smash.gg with a billion API requests*

####Future Goals:
* ~~Scrape the smash.gg api to get tournament results~~
* Make the glicko calculator standalone (maybe a python package?)
* ~~Output the results to a csv~~
* Add a predictor for a head to head given current Glicko ratings
* Use the predictor to model the likelihood of player X winning tournament Y
