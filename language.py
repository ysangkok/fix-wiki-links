# /* vim: tabstop=4:expandtab */
import webbrowser
from pywikibot import pagegenerators

import mwparserfromhell
import pywikibot

if __name__ == "__main__":
    site = pywikibot.Site(code='en')
    pages = site.exturlusage("www.language-museum.com")
    pages = pagegenerators.PreloadingGenerator(pages)
    for p in pages:
        print(p.title())
        if (p.namespace() != 0):
             print("skipping")
             continue
        parsed = mwparserfromhell.parse(p.text)
        didEdit = False
        for i in parsed.ifilter_external_links():
            if not i.url.startswith("http://www.language-museum.com"):
                continue
            if i.url in ["http://www.language-museum.com", "http://www.language-museum.com/"]:
                continue
            if i.url.startswith("http://www.language-museum.com/encyclopedia"):
                continue
            print(i)
            url = str(i.url).replace("language-museum.com", "language-museum.com/encyclopedia")

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
            p.save("fix language-museum.com link using MementoWeb")
