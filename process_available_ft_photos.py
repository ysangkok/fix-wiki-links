# vim: tabstop=4:expandtab
import webbrowser
from pywikibot import pagegenerators

import mwparserfromhell
import pywikibot
import os

with open('available.txt') as f:
    site = pywikibot.Site(code='da')

    for line in f.readlines():
        filename, separator, person_name = line.partition(' ', )
        person_name = person_name.rstrip()
        p = pywikibot.Page(title=person_name, source=site)
        try:
            p.get()
        except:
            print(f'{person_name} has no article')
            continue
        if 'Gammelt portræt' in p.text:
            print(f'{person_name} has link')
            continue
        os.system(f'echo "* [http://webarkiv.ft.dk/billeder/foto/{filename} Gammelt portrætfoto]" | xclip -sel clipboard /dev/stdin')
        webbrowser.open(f'https://da.wikipedia.org/w/index.php?title={p.title()}&action=edit')
        input('continue?')
