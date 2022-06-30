#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Get continent data including bounding boxes and centroids for and store it
# in json file keyed by continentCode.
import os
import json
import httpx

from pathlib import Path


# see http://download.geonames.org/export/dump/readme.txt
continent_ids = [6255146, 6255147, 6255148, 6255149, 6255151, 6255150, 6255152]
url = 'http://api.geonames.org/getJSON'
params = {
    'formatted': 'true',
    'username': os.environ['GEONAMES_USER'],
    'geonameId': None
}
continents = {}


def account_ok(j):
    if j.get(u'status', {}).get(u'value') == 10:
        print(j[u'status'][u'message'])
        exit(1)


for geoid in continent_ids:
    params['geonameId'] = geoid
    resp = httpx.get(url, params=params)
    if resp.is_success:
        cont = json.loads(resp.text)
        account_ok(cont)
        continents[cont['continentCode']] = cont


Path('data', 'continents.json').write_text(json.dumps(continents))
