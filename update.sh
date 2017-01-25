#!/bin/sh
#This script will do the following, in order:
#	Scrape data from a list of tournaments (./data/slugs.csv)
#	Fix the names specified in ./data/name_fixes.csv
#	!Move the data to the smash-site folder
#	!Compile a list of possible interesting matches
activate
python ./smashgg-scraper/get_data.py
python ./data/name_fixes.py
