# vim: tabstop=4:expandtab
import webbrowser
from pywikibot import pagegenerators

import mwparserfromhell
import pywikibot

if __name__ == "__main__":
    site = pywikibot.Site(code='da')
    pages = site.exturlusage("www.dr.dk/P")
    #if namespaces:
    #    pages = pagegenerators.NamespaceFilterPageGenerator(pages, namespaces)
    pages = pagegenerators.PreloadingGenerator(pages)
    for p in pages:
        print(p.title())
        if (p.namespace() != 0):
             print("skipping")
             continue
        parsed = mwparserfromhell.parse(p.text)
        didEdit = False
        for i in parsed.ifilter_external_links():
            if not i.url.startswith("http://www.dr.dk/P"):
                continue
            if i.url.startswith("http://www.dr.dk/P4"):
                continue
            print(i)
            url = "https://web.archive.org/web/20070706040605/" + str(i.url)
            #archive = requests.get("http://archive.org/wayback/available", params={"url": i.url, "timestamp": "08092010"}).json()
            #print(archive)
            #if not "closest" in archive["archived_snapshots"]:
            #    print("missing closest, skipping")
            #    continue
            #if not "timestamp" in archive["archived_snapshots"]["closest"]:
            #    print("missing timestamp, skipping")
            #    continue
            #timestamp = archive["archived_snapshots"]["closest"]["timestamp"]
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
            p.save("Reparér link til dr.dk")
