# HS-Playoff-Deck-Export

A python script for converting Hearthstone deck codes from a csv to deck images.

## Requirements

* Python 3.6+
* [python-hearthstone](https://github.com/hearthsim/python-hearthstone)
* [Python Imaging Library](https://pillow.readthedocs.io)
* [backports.csv](https://pypi.python.org/pypi/backports.csv)

## Setup

Please clone the repo here [https://github.com/HearthSim/hs-card-tiles](https://github.com/HearthSim/hs-card-tiles) and move the `Tiles` directory in the repo to `decktoimage/`.

If this repo hasn't been updated recently, update the current hs.cards.collectible.json to the one found at [https://api.hearthstonejson.com/v1/latest/](https://api.hearthstonejson.com/v1/latest/).

## Usage

```
usage: decktoimage.py [-h] [--ordered] deckcsv destination

create deck images from a csv file

positional arguments:
  deckcsv      the csv file containing all the decklists. The first line must
               be the schema, and all other lines must follow the schema
  destination  where the images are generated

optional arguments:
  -h, --help   show this help message and exit
  --ordered    set whether images should be grouped by the first letter of the
               key
```

## CSV formatting

The first line in the CSV file will be the schema for the rest of the file. It will be a comma separated list of arguments with the same length as the rest of the rows of the file. Leave unused fields blank, and use "K" for keys (which will group the decklists and control what the image file is named as), and "D" for deck codes to be parsed by the script.

For example, a schema of `K,D,D,D,D` in the first line of the csv will indicate that the followings lines have the form "Name/Key, Deck Code #1, Deck Code #2, Deck Code #3, Deck Code #4", which a schema of "K,,D" will indicate the form of "Name/Key, \[Irrelevant\], Deck Code" and the program will group deck codes corresponding to the same key to the same deck image.

## Example Usage

Example image generated using the following input:
```
K,D,D,D,D
killinallday#1537,AAECAZICCLQF3gWvwgLTxQLCzgKZ0wKc4gLQ5wIL8gWXwQKfwgLrwgKbywKHzgKR0ALR4QL55gLX6wKL7gIA,AAECAZ8FBNkHucECt+kCzfQCDfsBmQLcA/IF9AWWBs8GigevB7EIlgmbywL40gIA,AAECAaIHBJsFhsICz+ECw+oCDcQBnALtAp8DiAXUBYYJl8EC/MEC68ICx9MC2+MC9uwCAA==,AAECAf0GBpMEycICl9MC2OcC2+kCnPgCDIoB9wS2B5vCAufLAvLQAvjQAojSAovhAvzlAurmAujnAgA=
```
![killinallday deck image](https://imgur.com/9Yr0CCd.jpg "killinallday deck image")

