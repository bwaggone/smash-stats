## Smash.gg API Scraper

###Usage Instrucitons
Once you have the dependencies installed, run,
```
python get_data.py
```
You will see the following prompt:
```
Single Mode (s)? Or File Mode (f)?
```
Type in an 's' or 'f' to specify your choice. Single mode will allow you to type the url portion of the tournament for scraping. (smash.gg/**g4**) File mode will look at the [slugs.csv](../data/slugs.csv) file located in ./data/slugs.csv to scrape from. Single mode will give visual feedback for the scraping in the form of a progress bar, while File mode will tell you how many tournaments it has left to work through. All the csv files will be stored in their appropriate ./data/ directory. For formatting and csv styling, see [the appropriate readme.](../data/README.md)

#### How it works
Please see [smash.gg's documentation on their api](https://help.smash.gg/hc/en-us/articles/217471947-API-Access). The tldr is that given a tournament slug (portion of the url that smash.gg uses to identify tournaments), this scraper will get the list of events, entrants, and match those up to record the standings, wins, losses, and even game count (if applicable) for each game. This *does not* scrape non-smash games currently. It will skip over side events (around the world for Smash Summit 3, own the house for The Big House 6, etc...), but it's not perfect, and if you find an exception, DM me or submit an issue.

#### Dependencies
  * requests
  * progressbar
  * Check [requirements.txt](../requirements.txt) for full information.
