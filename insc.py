import webbrowser
from pywikibot import pagegenerators
import requests
import urllib.parse

import mwparserfromhell
import pywikibot

"""
following addition to pywikibot: pywikibot/families/haskellwiki_family.py:

from pywikibot import family

class Family(family.Family):
    name = 'haskellwiki'
    langs = {
        'en': 'wiki.haskell.org',
    }
    def scriptpath(self, code):
        return 'https://wiki.haskell.org/'


following changes to pywikibot/site.py


5285                 elif result['edit']['result'] == 'Failure':¬
5286                     if 'captcha' in result['edit']:¬
5287                         if not pywikibot.config.solve_captcha:¬
5288                             raise CaptchaError('captcha encountered while '¬
5289                                                'config.solve_captcha is False')¬
5290                         captcha = result['edit']['captcha']¬
5291                         req['captchaid'] = captcha['id']¬
5292                         if captcha['type'] == 'simple':¬
5293                             # TODO: Should the input be parsed through eval¬
5294                             # in py3?¬
5295                             import ast¬
5296                             req['captchaword'] = ast.literal_eval(captcha['question'].replace("−","-"))¬
5297                             continue
"""

def resolve_url(base_url):
    print(base_url)
    r = requests.get(base_url)
    print(r)
    return r.url

cache = {}

if __name__ == "__main__":
    site = pywikibot.Site(url='https://wiki.haskell.org/')
    pages = site.exturlusage("article.gmane.org")
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
            if 'gmane' not in i.url:
                continue
            print(i)
            url = "http://timetravel.mementoweb.org/memento/2019/" + str(i.url)
            #archive = requests.get("http://archive.org/wayback/available", params={"url": i.url, "timestamp": "08092010"}).json()
            #print(archive)
            #if not "closest" in archive["archived_snapshots"]:
            #    print("missing closest, skipping")
            #    continue
            #if not "timestamp" in archive["archived_snapshots"]["closest"]:
            #    print("missing timestamp, skipping")
            #    continue
            #timestamp = archive["archived_snapshots"]["closest"]["timestamp"]
            if url in cache:
                if cache[url]:
                    i.url = cache[url]
                    didEdit = True
                continue

            resolved_url = resolve_url(url)
            webbrowser.open(resolved_url)
            if "y" == pywikibot.input_choice('\nFix THIS link?', [('yes', 'y'), ('no', 'n')], 'n', automatic_quit=False):
                print("accepted")
                i.url = resolved_url
                didEdit = True
                cache[url] = resolved_url
            else:
                print("rejected")
                cache[url] = False
        if didEdit:
            if "y" != pywikibot.input_choice('\nEdit and save page {}?'.format(p.title()), [('yes', 'y'), ('no', 'n')], 'n', automatic_quit=False): continue
            p.text = str(parsed)
            p.save("fix gmane link using MementoWeb")
