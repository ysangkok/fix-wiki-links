# /* vim: tabstop=4:expandtab */
import webbrowser
import requests
import requests.exceptions
from pywikibot import pagegenerators

import mwparserfromhell
from mwparserfromhell.nodes.external_link import ExternalLink
from mwparserfromhell.nodes.template import Template
import pywikibot

urls = {}

def get_choice(url):
    if not url in urls:
        ans = pywikibot.input_choice('\nFix THIS link and remove dead link template?', [('yes', 'y'), ('no', 'n')], 'n', automatic_quit=False)
        urls[url] = ans
    else:
        ans = urls[url]
    return ans

if __name__ == "__main__":
    site = pywikibot.Site(code='en')
    pages = pywikibot.Category(source=site, title="Category:Articles with dead external links from January 2010").articles()
    for p in pages:
        print(p.title())
        if (p.namespace() != 0):
             print("skipping, namespace {}".format(p.namespace()))
             continue
        parsed = mwparserfromhell.parse(p.text)
        didEdit = False
        for i in parsed.ifilter(forcetype=(ExternalLink, Template)):
            if type(i) is ExternalLink:
                link = i
                continue
            # i is a template invocation
            if not i.name.matches("dead link"):
                print("skipping, template name is {}".format(i.name))
                continue

            print(link.url)

            catched = False
            res = None
            try:
                res = requests.head(str(link.url), timeout=10)
                print(res.status_code)
            except (requests.exceptions.ReadTimeout, requests.ConnectionError) as e:
                print(e)
                catched = True
            except Exception as e:
                print(e.get_message())
                catched = True
            if not catched and res.status_code == 200:
                ans = pywikibot.input_choice('\nLINK IS OK. Remove dead link template?', [('yes', 'y'), ('no', 'n')], 'n', automatic_quit=False)
                if "y" == ans:
                    parsed.remove(i)
                    didEdit = True
                    continue

            fixurl = "http://timetravel.mementoweb.org/memento/2010/" + str(link.url)
            webbrowser.open(fixurl)

            if "y" == get_choice(str(link.url)):
                print("accepted")
                link.url = fixurl
                parsed.remove(i)
                didEdit = True
            else:
                print("rejected")
        if didEdit:
            if "y" != pywikibot.input_choice('\nEdit and save page {}?'.format(p.title()), [('yes', 'y'), ('no', 'n')], 'n', automatic_quit=False): continue
            p.text = str(parsed)
            p.save("fix links using ysangkok/fix-wiki-links")
