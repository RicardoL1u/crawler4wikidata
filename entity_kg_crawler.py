import requests
import json
from tqdm import tqdm
with open('entity_list.txt') as f:
    entity_list = f.read().splitlines()

entity_list = list(set(entity_list))
with open('/data/lyt/wikidata-5m/wiki5m_dict_update.json') as f:
    wiki5m_dict = json.load(f)

failed_entity_list = []
for entity in tqdm(entity_list):
    try:
        if entity in wiki5m_dict:
            continue
        entity_info = requests.get(f'https://www.wikidata.org/wiki/Special:EntityData/{entity}.json').json()
        wiki5m_dict[entity] = {}
        # cralwer all the properties of entity
        # save as wiki5m_dict[entity][property] = [value1, value2, ...]
        for property in entity_info['entities'][entity]['claims']:       
            relation = entity_info['entities'][entity]['claims'][property][0]['mainsnak']['property']
            if relation not in wiki5m_dict[entity]:
                wiki5m_dict[entity][relation] = []
            
            for tail in entity_info['entities'][entity]['claims'][property]:
                # only care about the entity related
                if tail['mainsnak']['snaktype'] == 'value' and \
                    tail['mainsnak']['datavalue']['type'] == 'wikibase-entityid':
                    value = tail['mainsnak']['datavalue']['value']['id']
                    wiki5m_dict[entity][relation].append(value)
            if wiki5m_dict[entity][relation] == []:
                del wiki5m_dict[entity][relation]
        print(wiki5m_dict[entity])
    except Exception as e:
        print(e)
        failed_entity_list.append(entity)
        continue
with open('failed_entity_list.txt', 'w') as f:
    f.write('\n'.join(failed_entity_list))

with open('/data/lyt/wikidata-5m/wiki5m_dict_update.json', 'w') as f:
    json.dump(wiki5m_dict, f)