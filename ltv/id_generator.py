import datetime
import dataset


NUM_SHOWS = 35000
db = dataset.connect('postgresql+psycopg2://postgres@localhost/legendastvmirror')

def run(num_shows=NUM_SHOWS):
    table = db['shows']
    db.begin()
    for x in xrange(1, num_shows):
        reg = dict(show_id=x, exists=None, last_change_time=datetime.datetime.min, show_name='', status='')
        table.insert(reg, ensure=False)
    db.commit()

if __name__ == '__main__':
    run()
