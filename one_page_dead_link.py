# /* vim: tabstop=4:expandtab */
import webbrowser
import requests
from pywikibot import pagegenerators, i18n
from pywikibot.editor import TextEditor

import mwparserfromhell
import pywikibot

if __name__ == "__main__":
    site = pywikibot.Site(code='en')
    pages = [pywikibot.Page(source=site, title="Vogtle Electric Generating Plant")]
    for p in pages:
        print(p.title())
        if (p.namespace() != 0):
             print("skipping")
             continue
        parsed = mwparserfromhell.parse(p.text)
        didEdit = False
        for i in parsed.ifilter_external_links():
            print(i.url)
            catched = False
            res = None
            try: res = requests.get(i.url)
            except Exception as e:
                print(e.get_message())
                catched = True
            print(res.status_code)
            if res.status_code == 200: continue
            url = "http://timetravel.mementoweb.org/memento/2010/" + str(i.url)
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
