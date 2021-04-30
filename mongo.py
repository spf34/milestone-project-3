import os
import pymongo

if os.path.exists('env.py'):
    import env

MONGO_URI = os.environ.get('MONGO_URI')
DATABASE = 'OPT'
COLLECTION = 'users'


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print('Mongo is connected')
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print(f'Could not connect to MongoDB: {e}')


conn = mongo_connect(MONGO_URI)

coll = conn[DATABASE][COLLECTION]

sf = {
    'first': 'Samuel',
    'last': 'Forster',
    'email': 'samuel.p.forster@gmail.com',
    'user_id': 1,
    }

jl = {
    'first': 'Jesse',
    'last': 'Livermore',
    'email': 'j.livermore@gmail.com',
    'user_id': 2,
    }

dh = {
    'first':  'David',
    'last': 'Harding',
    'email': 'david.harding@winton.com',
    'user_id': 3,
    }

# new_docs = [sf, jl, dh]

# coll.insert_many(new_docs)
# coll.delete_one(dh)

# coll.update_one({'first': 'David'}, {'$set': {'last': 'X', 'email': 'DavidX@X.com'}})

# documents = coll.find({'first': 'David'})

documents = coll.find()
print(type(documents))
print(len(documents))

for doc in documents:
    print(doc)
