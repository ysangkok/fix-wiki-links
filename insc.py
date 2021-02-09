import webbrowser
from pywikibot import pagegenerators
import requests
import urllib.parse
import re

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
    print("Resolving", base_url)
    r = requests.get(base_url, headers={'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'})
    match = re.search("\"(http://archive.fo/[a-z0-9A-Z]{5})\"", r.text)
    if match:
        url = match.group(1)
        print("Resolved", url)
        return url
    print("not found in text")
    return None

cache = {}

if __name__ == "__main__":
    site = pywikibot.Site('en')
    pages = site.exturlusage("www.businessweek.com/1997")
    #if namespaces:
    #    pages = pagegenerators.NamespaceFilterPageGenerator(pages, namespaces)
    pages = pagegenerators.PreloadingGenerator(pages)
    skip_until = "Massachusetts Miracle"
    skip = True
    for p in pages:
        print(p.title())
        if skip:
            if p.title() != skip_until:
                continue
            else:
                skip = False
        if (p.namespace() != 0):
             print(f"skipping namespace {p.namespace()}")
             continue
        parsed = mwparserfromhell.parse(p.text)
        didEdit = False
        for i in parsed.ifilter_external_links():
            if 'businessweek' not in i.url or "archive.org" in i.url:
                continue
            print(i)
            url = "http://archive.fo/" + str(i.url)
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
            if not resolved_url:
                print("COULD NOT resolve, skipping")
                continue
            resp = resolved_url
            #resp = input('\nFix THIS link? (or paste URL)\n')
            #if not resp:
            #    print("rejected")
            #    cache[url] = False
            #    continue
            #if resp == "y":
            #    resp = resolved_url
            #print("accepted")
            i.url = resp
            didEdit = True
            cache[url] = resp
        if didEdit:
            webbrowser.open(p.full_url())
            if "y" != pywikibot.input_choice('\nEdit and save page {}?'.format(p.title()), [('yes', 'y'), ('no', 'n')], 'n', automatic_quit=False): continue
            p.text = str(parsed)
            p.save("fix businessweek links using archive.fo")
