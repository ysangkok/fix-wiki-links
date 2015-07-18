lol: core
	PYTHONPATH=core python3 one_page_dead_link.py

core:
	git clone --branch 2.0 --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git
