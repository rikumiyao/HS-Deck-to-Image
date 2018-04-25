# HS-Playoff-Deck-Export

A python script for converting Hearthstone deck codes from a csv to deck images.

## Requirements

* Python 2.7+
* [python-hearthstone](https://github.com/hearthsim/python-hearthstone)
* [Python Imaging Library](http://www.pythonware.com/products/pil/)
  * If you are using Python 3 use the fork [link](https://pillow.readthedocs.io)
* [backports.csv](https://pypi.python.org/pypi/backports.csv)

## Installation
TODO

## To Run

Please download tiles from [https://github.com/HearthSim/hs-card-tiles](https://github.com/HearthSim/hs-card-tiles) and put in Tiles directory.

Each line in the CSV file should be of the format "Name, Deck code #1, Deck code #2, Deck code #3, Deck code #4"
The ipython notebook uses decklists.csv as the default source and /decks (Create this yourself) as the default directory. However, running decktoimage.py allows you to specify command line parameters.

To run the python script, run `python decktoimage.py CSVFILE DESTDIRECTORY`
WARNING: The files in DESTDIRECTORY will be cleared to leave room for alphabetical deck directories.

Used in for various official Hearthstone tournaments, including HCT Tour Stops, HCT Playoffs, and Tespa Championships.

Example image generated:  
![YAYtears deck image](https://imgur.com/HApi5AW.jpg "YAYtears deck image")

