# /* vim: tabstop=4:expandtab */
import webbrowser
import requests
from pywikibot import pagegenerators

import mwparserfromhell
from mwparserfromhell.nodes.external_link import ExternalLink
from mwparserfromhell.nodes.template import Template
import pywikibot

if __name__ == "__main__":
    site = pywikibot.Site(code='en')
    pages = pywikibot.Category(source=site, title="Category:Articles with dead external links from June 2008").articles()
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
            webbrowser.open(link.url)

            if "y" == pywikibot.input_choice('\nFix THIS link?', [('yes', 'y'), ('no', 'n')], 'n', automatic_quit=False):
                print("accepted")
                link.url = "http://timetravel.mementoweb.org/memento/2010/" + str(link.url)
                i.remove()
                didEdit = True
            else:
                print("rejected")
        if didEdit:
            if "y" != pywikibot.input_choice('\nEdit and save page {}?'.format(p.title()), [('yes', 'y'), ('no', 'n')], 'n', automatic_quit=False): continue
            p.text = str(parsed)
            p.save("fix links using ysangkok/fix-wiki-links")
