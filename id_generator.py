from couchdb.client import Server
NUM_SHOWS = 35000
server = Server('http://localhost:5984/')
db = server['legendastvmirror']
ids_list = []

for x in xrange(1, NUM_SHOWS):
    doc = dict(show_id=x, exists=None, last_checked=0, type='IdGenerator')
    db.save(doc)
