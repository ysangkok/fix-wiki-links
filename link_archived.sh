#!/usr/bin/env bash
set -euo pipefail
curl 'http://web.archive.org/cdx/search/cdx?url=http://www.ft.dk/billeder/foto/*&output=json' > archived.json
for i in $(jq -r '.[] | .[2]' < archived.json | grep -i htm$ | cut -d/ -f6 | uniq); do
		OUT="$(curl -sf webarkiv.ft.dk/billeder/foto/$i)"
		if [[ $? == 0 ]]; then
				echo $i $(echo $OUT | iconv -fiso8859-1 -tutf-8 | grep title | sed -re 's#<head><title>([A-Za-z \.-]*)</title></head>#\1#g') | tee -a available.txt
		else
				echo $i | tee -a not_available.txt
		fi
done
