import requests
import json
from tqdm import tqdm
with open('entity_list.txt') as f:
    entity_list = f.read().splitlines()

entity_list = list(set(entity_list))
with open('/data/lyt/wikidata-5m/wikidata-5m-entity-en-label.json') as f:
    entity_label_dict = json.load(f)

failed_entity_list = []
for entity in tqdm(entity_list):
    try:
        if entity in entity_label_dict:
            continue
        entity_info = requests.get(f'https://www.wikidata.org/wiki/Special:EntityData/{entity}.json').json()
        entity_label_dict[entity] = {}
        entity_label_dict[entity]['label'] = entity_info['entities'][entity]['labels']['en']['value']
        entity_label_dict[entity]['description'] = entity_info['entities'][entity]['descriptions']['en']['value']
        entity_label_dict[entity]['altLabel'] = [alias['value'] for alias in entity_info['entities'][entity]['aliases']['en']]
        print(entity_label_dict[entity])
    except Exception as e:
        print(e)
        failed_entity_list.append(entity)
        continue
with open('failed_entity_list.txt', 'w') as f:
    f.write('\n'.join(failed_entity_list))

with open('/data/lyt/wikidata-5m/wikidata-5m-entity-en-label.json', 'w') as f:
    json.dump(entity_label_dict, f)