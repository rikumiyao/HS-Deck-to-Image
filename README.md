# HS-Playoff-Deck-Export

A python script for converting Hearthstone deck codes from a csv to deck images.

## Requirements

* Python 3.6+
* [python-hearthstone](https://github.com/hearthsim/python-hearthstone)
* [Python Imaging Library](https://pillow.readthedocs.io)
* [backports.csv](https://pypi.python.org/pypi/backports.csv)

## Installation
TODO

## To Run

Please download tiles from [https://github.com/HearthSim/hs-card-tiles](https://github.com/HearthSim/hs-card-tiles) and put in Tiles directory.

The first line in the CSV file will be the schema for the rest of the file. It will be a comma separated list of arguments with the same length as the rest of the rows of the file. Leave unused fields blank, and use "K" for keys (which will group the decklists and control what the image file is named as), and "D" for deck codes to be parsed by the script.

For example, a schema of "K,D,D,D,D" in the first line of the csv will indicate that the followings lines have the form "Name/Key, Deck Code #1, Deck Code #2, Deck Code #3, Deck Code #4", which a schema of "K,,D" will indicate the form of "Name/Key, \[Irrelevant\], Deck Code" and the program will group deck codes corresponding to the same key to the same deck image.

To run the python script, run `python decktoimage.py CSVFILE DESTDIRECTORY`
The DESTDIRECTORY will be created if it doesn't exist and the contents of the directory will not be overwritten if it already exists, so make sure to clear the directory first if you want to create new deck images.

Used in for various official Hearthstone tournaments, including HCT Tour Stops, HCT Playoffs, and Tespa Championships.

Example image generated:  
![killinallday deck image](https://imgur.com/9Yr0CCd "YAYtears deck image")

