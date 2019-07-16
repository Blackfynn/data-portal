from config import Config

from blackfynn import Blackfynn
from pymongo import MongoClient

import dateutil.parser

# Constants:
SPARC_ORG_ID = 'N:organization:618e8dd9-f8d2-4dc4-9abb-c6aaab2e78a0'
MONGODB_URI = 'mongodb://localhost:27017'
DB_NAME = 'sparc-embargo'
COLLECTION_NAME = 'sparc-embargo'

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
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
embargoed = db[COLLECTION_NAME]
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
        # 'modelCount': {x['name']: x['count'] for x in bf._api.concepts._get(api._uri('/{dsid}/concepts', dsid=content['id']))},
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

### Delete all entries:
embargoed.drop()

### Then add all unpublished datasets:
for ds in all_datasets:
    if ds['content']['intId'] not in publishedIds:
        entry = transform(ds)
        inserted = embargoed.update_one({'_id': entry.pop('_id')}, {'$set': entry}, upsert=True)
        print('Added:', inserted.upserted_id, entry['name'], sep='\t')

print('Sync finished.')