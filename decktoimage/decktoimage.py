
# coding: utf-8

# # Created by Riku Miyao (@YAYtears)

from backports import csv
from hearthstone.deckstrings import Deck
from hearthstone.deckstrings import FormatType
import json
#Python3 version https://pillow.readthedocs.io
from PIL import Image, ImageDraw, ImageFont
import io
import sys
import os
import shutil
import re


#https://github.com/HearthSim/hs-card-tiles
tile_url = 'Tiles/'

#https://api.hearthstonejson.com/v1/latest/enUS/cards.collectible.json
cards_json = 'cards.collectible.json'
#stolen from https://deck.codes/ which was probably stolen from Hearthstone or HDT
tile_container_number = 'resources/tile_container_number.png'
tile_container_open = 'resources/tile_container_open.png'
star = 'resources/star.png'

deck_font = 'resources/Belwe-Bold.ttf'
name_font = 'resources/NotoSansCJK-Bold.ttc'

card_dict = {}
with open(cards_json, encoding="utf-8") as json_file:
    data = json.load(json_file)
    for card in data:
        card_dict[card['dbfId']] = card

def interpolate_color(minval, maxval, val, color_palette):
    """ Computes intermediate RGB color of a value in the range of minval-maxval
        based on color_palette representing the range. """
    #stack overflow is bae
    max_index = len(color_palette)-1
    v = float(val-minval) / float(maxval-minval) * max_index
    i1, i2 = int(v), min(int(v)+1, max_index)
    (r1, g1, b1, a1), (r2, g2, b2, a2) = color_palette[i1], color_palette[i2]
    f = v - i1
    return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1)), int(a1 + f*(a2-a1))
def draw_shadow(draw,x,y,text,font,shadowcolor="black"):

    # thin border
    draw.text((x-1, y-1), text, font=font, fill=shadowcolor)
    draw.text((x+1, y+1), text, font=font, fill=shadowcolor)
    draw.text((x+1, y-1), text, font=font, fill=shadowcolor)
    draw.text((x-1, y+1), text, font=font, fill=shadowcolor)

def find_code(text):
    line = text.strip()
    for x in line.split(' '):
        if x.startswith('AAE'):
            return x
    return line
def parse_deck(text):
    for i in range(3):
        try:
            deck = Deck.from_deckstring(text+'='*i)
            return deck
        except Exception as e:
            continue
    return None
def deck_to_image(deck, name):
    if deck.heroes[0]==1325:
        deck.heroes[0] = 637 #idk where this came from but apparently its mage lol
    if deck.heroes[0] not in card_dict:
        print(deck.as_deckstring)
    hero = card_dict[deck.heroes[0]]
    imclass = Image.open('resources/{}.jpg'.format(hero['cardClass'].lower()))
    cards = [(card_dict[x[0]],x[1]) for x in deck.cards]
    cards.sort(key = lambda x:(x[0]['cost'], x[0]['name']))
    width = 243
    height = 39 * len(cards) + imclass.size[1]
    xoff = 105
    
    master = Image.new('RGBA', (width, height))
    for index, (card, count) in enumerate(cards):
        image = '{}{}.png'.format(tile_url, card['id'])
        im = Image.open(image)
        minx = 105
        maxx = 221
        color_palette = [(41,48,58,255), (93, 68, 68, 0)]
        master.paste(im, (xoff,3+39*index, xoff+130, 39*(index+1)-2))

        gradient = Image.new('RGBA', (width, height))
        draw = ImageDraw.Draw(gradient)
        for x in range(20, minx):
            draw.line([(x, 39*index), (x, 39*(index+1))], fill=color_palette[0])
        for x in range(minx, maxx):
            color = interpolate_color(minx, maxx, x, color_palette)
            draw.line([(x, 39*index), (x, 39*(index+1))], fill=color)
        
        master = Image.alpha_composite(master, gradient)
        draw = ImageDraw.Draw(master)
        font = ImageFont.truetype(deck_font, 15)

        draw_shadow(draw, 39, 13+39*index, card['name'],font)
        draw.text((39, 13+39*index), card['name'], font=font)

        if count==2:
            bg = Image.open(tile_container_number)
            master.paste(bg, (0,39*index, 239, 39*(index+1)), bg)
            font = ImageFont.truetype(deck_font, 16)
            w, h = draw.textsize('2', font=font)
            draw.text(((30-w)/2+209,(39-h)/2+39*index), '2', font=font, fill=(229, 181, 68))
        elif card['rarity']=='LEGENDARY':
            bg = Image.open(tile_container_number)
            master.paste(bg, (0,39*index, 239, 39*(index+1)), bg)
            imstar = Image.open(star)
            master.paste(imstar, (214, 39*index+10, 233, 39*index+29), imstar)
        else:
            bg = Image.open(tile_container_open)
            master.paste(bg, (0,39*index, 239, 39*(index+1)), bg)
        msg = str(card['cost'])
        w, h = draw.textsize(msg, font=font)
        font = ImageFont.truetype(deck_font, 16)
        draw_shadow(draw,(34-w)/2,(39-h)/2+39*index,str(card['cost']), font)
        draw.text(((34-w)/2, (39-h)/2+39*index), str(card['cost']), font=font)
        #draw.text()
    decklist = master.crop((0,0,243,39*len(cards)))
    master.paste(decklist, (0,97,243,39*len(cards)+97))
    master.paste(imclass, (0,0,243,97))
    font = ImageFont.truetype(name_font, 19)
    #title = u'{} {}'.format(name, hero['playerClass'][0]+hero['playerClass'][1:].lower())
    title = name
    w,h = draw.textsize(title, font=font)
    draw_shadow(draw, 22, 75-h, title, font)
    draw.text((22, 75-h), title, font=font)
    return master

def merge(imgs):
    width = sum(x.size[0] for x in imgs)
    height = max(x.size[1] for x in imgs)
    master = Image.new('RGBA', (width, height))
    x = 0
    for img in imgs:
        w,h = img.size
        master.paste(img, (x, 0, x+w, h), img)
        x+=w
    return master

def setup_dirs(url):
    if not os.path.exists(url):
        os.makedirs(url)
    for x in range(ord('A'),ord('Z')+1):
        addr = '{}/{}'.format(url,chr(x))
        if not os.path.exists(addr):
            os.makedirs(addr)
    addr = '{}/{}'.format(url,'etc')
    if not os.path.exists(addr):
        os.makedirs(addr)
    addr = '{}/{}'.format(url,'_All')
    if not os.path.exists(addr):
        os.makedirs(addr)

def process(decklists, deck_url):
    setup_dirs(deck_url)
    all_names = {}
    with io.open(decklists, "r", encoding="utf-8") as csvfile:
        deckreader = csv.reader(csvfile, delimiter=u',')
        deckreader = list(deckreader)
        fail = ''
        schemaLine = deckreader[0]
        schema = []
        key = 0
        for index, x in enumerate(schemaLine):
            if x=='D':
                schema.append('D')
            elif x=='K':
                schema.append('K')
                key = index
            else:
                schema.append('')
        for row in deckreader[1:]:
            name = row[key]
            name = name.replace('/','\\')
            if name not in all_names:
                all_names[name] = []
            for index, a in enumerate(schema):
                if a!='D':
                    continue
                decklist = find_code(row[index])
                deck = parse_deck(decklist)
                all_names[name].append(deck)
        for name in all_names:
            deck_imgs = []
            for deck in all_names[name]:
                if deck!=None:
                    img = deck_to_image(deck, name)
                    deck_imgs.append(img)
            img = merge(deck_imgs)
            img = img.convert('RGB')
            if (ord(name[0].upper())>=ord('A') and ord(name[0].upper())<=ord('Z')):
                img.save(u'{}/{}/{}.jpg'.format(deck_url,name[0].upper(),name), 'JPEG')
            else:
                img.save(u'{}/{}/{}.jpg'.format(deck_url,'etc',name), 'JPEG')
            img.save(u'{}/{}/{}.jpg'.format(deck_url,'_All',name), 'JPEG')


#Where the images are generated. This directory is not cleared when the program
#is run, and the contents of the directory are not overwritten
if __name__=="__main__":
    if len(sys.argv)!=3:
        print("Usage: python decktoimage.py deckcsv destination")
    else:
        process(sys.argv[1], sys.argv[2])

