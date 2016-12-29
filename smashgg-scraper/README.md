## Smash.gg API Scraper

#### How it works
Please see [smash.gg's documentation on their api](https://help.smash.gg/hc/en-us/articles/217471947-API-Access). The tldr is that given a tournament slug (portion of the url that smash.gg uses to identify tournaments), this scraper will get the list of events, entrants, and match those up to record the standings, wins, losses, and even game count (if applicable) for each game. This *does not* scrape non-smash games currently. It will skip over events that are not traditional smash events (around the world for Smash Summit 3, own the house for The Big House 6, etc...), but it's not perfect (genesis 3 has an event or two that confuses it).

#### Dependencies
  * requests
  * progressbar
  * Check [requirements.txt](../requirements.txt) for full information.
