import json
from bs4 import BeautifulSoup
import requests
url2qid_dict = json.load(open('/data/lyt/wikidata-5m/url2qid.json'))


url_list = list(set(open('url_list.txt').read().splitlines()))
# use bs4 get the wikidata id from wikipedia url
for url in url_list:
    wikidata_id = BeautifulSoup(requests.get(url).text, 'html.parser').find('li', {'id': 't-wikibase'}).find('a')['href'].split('/')[-1]
    url2qid_dict[url] = wikidata_id
    print(url, wikidata_id)

with open('/data/lyt/wikidata-5m/url2qid.json', 'w') as f:
    json.dump(url2qid_dict, f)

