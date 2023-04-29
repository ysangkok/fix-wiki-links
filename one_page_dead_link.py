# vim: tabstop=4:expandtab
import webbrowser
import requests
from requests.exceptions import ReadTimeout

import mwparserfromhell
import pywikibot

if __name__ == "__main__":
    site = pywikibot.Site(code='en')
    pages = [pywikibot.Page(source=site, title="Thou_shalt_not_covet")]
    for p in pages:
        print(p.title())
        if (p.namespace() != 0):
             print("skipping")
             continue
        parsed = mwparserfromhell.parse(p.text)
        didEdit = False
        for i in parsed.ifilter_external_links():
            if "va/archive/catechis" in i.url:
                continue
            print(i.url)
            catched = False
            res = None
            try: res = requests.get(i.url, timeout=2)
            except ReadTimeout:
                catched = True
            except Exception as e:
                print(e.get_message())
                catched = True
            else:
                print(res.status_code)
                if res.status_code == 200: continue
            url = "http://archive.is/timegate/" + str(i.url)
            webbrowser.open(url)
            if "y" == pywikibot.input_choice('\nFix THIS link?', [('yes', 'y'), ('no', 'n')], 'n', automatic_quit=False):
                print("accepted")
                i.url = url
                didEdit = True
            else:
                print("rejected")
        if didEdit:
            if "y" != pywikibot.input_choice('\nEdit and save page {}?'.format(p.title()), [('yes', 'y'), ('no', 'n')], 'n', automatic_quit=False): continue
            p.text = str(parsed)
            p.save("fix dead link using MementoWeb")
