#!/usr/bin/env python3

from config import Config

from blackfynn import Blackfynn
from pymongo import MongoClient

print('Starting embargoed data sync')

### Connect to Blackfynn
print('Connecting to Blackfynn ...', end=' ')
bf = Blackfynn(
    api_token=Config.BLACKFYNN_API_TOKEN,
    api_secret=Config.BLACKFYNN_API_SECRET,
    env_override=False,
    host=Config.BLACKFYNN_API_HOST,
)
api = bf._api.core
print('done')

### Connect to MongoDB
print('Connecting to MongoDB ...', end=' ')
client = MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_NAME]
embargoed = db[Config.MONGODB_COLLECTION]
print('done')

def transform(ds):
    'Convert dataset JSON from Blackfynn to a database entry'
    content = ds['content']
    models = bf.get_dataset(content['id']).models()
    org = api._get(api._uri('/organizations/{orgid}', orgid=ds['organization']))
    doc = {
        '_id': content['intId'],
        'name': content['name'],
        'description': content.get('description'),
        'createdAt': content['createdAt'],
        'updatedAt': content['updatedAt'],
        'tags': content['tags'],
        'contributors': content['contributors'],
        'organization': ds['organization'],
        'userId': ds['owner'],
        'size': ds['storage'],
        'organization': org['organization']['name'],
        'organizationId': org['organization']['intId'],
        'modelCount': {name: m.count for name,m in models.items()},
        'fileCount': {},
        'recordCount': sum(m.count for m in models.values()),
        'banner': api._get(api._uri('/datasets/{dsid}/banner', dsid=content['id'])).get('banner', None)
    }
    for p in api._get(api._uri('/datasets/{dsid}/packages', dsid=content['id']))['packages']:
        ptype = p['content']['packageType']
        c = doc['fileCount'].setdefault(ptype, 0)
        doc['fileCount'][ptype] = c + 1
    return doc

all_datasets = api._get('/datasets') # assuming all of these are part of SPARC Consortium org.
publishedIds = [x['sourceDatasetId'] for x in api._get('/datasets/published')]

### Delete all existing entries:
embargoed.drop()

for ds in all_datasets:
    # skip if dataset is published or isn't part of Embargoed Data Team:
    if ds['content']['intId'] in publishedIds or not any(t['id'] == Config.BLACKFYNN_EMBARGO_TEAM_ID for t in \
        api._get(api._uri('/datasets/{dsid}/collaborators/teams', dsid=ds['content']['id']))):
        continue
    entry = transform(ds)
    inserted = embargoed.update_one({'_id': entry.pop('_id')}, {'$set': entry}, upsert=True)
    print('Added:', inserted.upserted_id, entry['name'], sep='\t')

print('Sync finished.')