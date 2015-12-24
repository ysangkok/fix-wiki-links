lol: core
	PYTHONPATH=core python3 walk_cat.py

core:
	git clone --branch 2.0 --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git
