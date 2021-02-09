import datetime
import webbrowser
import requests
import re

from memento_client import MementoClient
import mwparserfromhell
from pywikibot import pagegenerators
import pywikibot

dt = datetime.datetime(2010, 4, 24, 19, 0)

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
    pages = site.exturlusage("www.newstatesman.com/1999")
    #if namespaces:
    #    pages = pagegenerators.NamespaceFilterPageGenerator(pages, namespaces)
    pages = pagegenerators.PreloadingGenerator(pages)
    skip_until = "Pan Am Flight 103"
    skip = False
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
            if 'newstatesman.com' not in i.url or "archive.org" in i.url:
                continue
            print(i)
            mc = MementoClient()
            url = str(i.url)
            if url not in cache:
                try:
                    nurl = mc.get_memento_info(url, dt)["mementos"]["closest"]["uri"][0]
                except KeyError:
                    continue
                print(f"old link {url}")
                print(f"new link {nurl}")
                cache[url] = i.url
            else:
                nurl = cache[url]
            webbrowser.open(p.full_url())
            if (inp := input("fix?").strip()) != "y":
                print(f"skipping because user input {inp}")
                continue
            i.url = nurl
            didEdit = True
        if didEdit:
            if "y" != pywikibot.input_choice('\nEdit and save page {}?'.format(p.title()), [('yes', 'y'), ('no', 'n')], 'n', automatic_quit=False): continue
            p.text = str(parsed)
            p.save("fix Newstatesman links using MementoWeb")
