#!/usr/bin/python3

import pywikibot
from pywikibot import pagegenerators as pg
import urllib.parse
import requests
import requests.exceptions

bot = pywikibot.bot.WikidataBot()

with open('pka-query.rq', 'r') as query_file:
    QUERY = query_file.read()

wikidata_site = pywikibot.Site("wikidata", "wikidata")
generator = pg.WikidataSPARQLPageGenerator(QUERY, site=wikidata_site)

prefix = 'https://www.ft.dk/medlemmer/mf/'

def killdanish(navn):
    return navn.replace('æ','ae').replace('ø','oe').replace('å','aa').replace("ö", 'oe')

# returns prop, url_ending
def slugify(navn):
    no_nameprefix = navn.lower().replace(' ','-').replace('.','').replace('--', '-')
    nameprefix = killdanish(navn.lower()[:1])
    url_ending = nameprefix + '/' + no_nameprefix
    if len(nameprefix.encode('utf-8')) == 1:
        return no_nameprefix, url_ending
    else:
        return url_ending, url_ending

assert slugify('Özlem') == ('oe/özlem', 'oe/özlem'), slugify('Özlem')
assert slugify('Per') == ('per', 'p/per')

for item in generator:
    item.get()
    print(item)
    try:
        lbl = item.labels['da']
    except KeyError:
        lbl = item.labels[next(iter(item.labels.keys()))]
    print(lbl)
    encoded = urllib.parse.urlencode({'q': "site:ft.dk " + lbl})
    print('http://google.com/search?' + encoded)
    #print(list(item.extlinks()))
    #gotten = item.get()
    #claims = gotten['claims']
    #print(claims)
    claim = pywikibot.Claim(wikidata_site, 'P7882')
    with open('blacklist.txt', 'r') as f:
        if item.id + '\n' in f.readlines():
            print("SKIPPING, IN BLACKLIST")
            continue
    prop_target, url_ending = slugify(lbl)
    try:
        code = requests.head(prefix + url_ending, timeout=2).status_code
    except requests.exceptions.ReadTimeout:
        print("TIMEOUT")
        code = 999
    print('status code', code)
    if not (299 >= code >= 200):
        prop_target = input('prop target?')
        if not prop_target:
            with open('blacklist.txt', 'a') as f:
                f.write(item.id + '\n')
            continue
        url_ending = prop_target[:1] + '/' + prop_target
        code = requests.head(prefix + url_ending).status_code
        assert 299 >= code >= 200, code
    claim.setTarget(prop_target)
    bot.user_add_claim(item, claim)
