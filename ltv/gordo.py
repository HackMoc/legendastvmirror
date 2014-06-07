# -*- coding: utf-8 -*-
import dataset
import datetime
import os
import requests
import sys
from multiprocessing import Pool


NUM_WORKERS = 10


class Gordo(object):

    def __init__(self, base_path, results):
        self.base_path = base_path
        self.db = dataset.connect('postgresql+psycopg2://postgres@localhost/legendastvmirror')
        self.shows = results
        self.release = None
        self.show = None

    def work(self):
        for show in self.shows:
            self.show = show
            last_change = datetime.datetime.strftime(
                datetime.datetime.now() + datetime.timedelta(minutes=20),
                '%Y-%m-%d %H:%M'
            )
            query = 'SELECT * FROM release \
                    WHERE show_id={show_id} AND (\
                        status="extracted" OR \
                        (status="downloading" AND last_change_time>={last_change})\
                    )'.format(show_id=self.show['id'], last_change=last_change)
            releases = list(self.db.query(query))
            for release in releases:
                self.release = release
                self.__download_subtitle()

    def __download_subtitle(self):
        self.db.begin()
        self.release['status'] = 'downloading'
        self.release['last_change_time'] = datetime.datetime.now()
        self.db['release'].update(self.release, ['id'], ensure=False)
        self.db.commit()
        subtitle = requests.get(url=self.release['subtitle_download_link']).content
        name = '[{language}]{slug}.rar'.format(language=self.release['language'], slug=self.release['slug'])
        filename = os.path.join([self.base_path, self.show['show_name'][0], self.show['show_name'], name])
        with open(filename, 'wb') as arquivo:
            arquivo.write(subtitle)
        self.db.begin()
        self.release['status'] = 'downloaded'
        self.release['last_change_time'] = datetime.datetime.now()
        self.db['release'].update(self.release, ['id'], ensure=False)
        self.commit()


def worker(results):
    base_path = sys.argv[1]
    g = Gordo(base_path, results)
    try:
        g.work()
    except Exception, ex:
        print "Exception {ex} ao tentar baixar {results}".format(ex=ex, results=results)


if __name__ == '__main__':
    db = dataset.connect('postgresql+psycopg2://postgres@localhost/legendastvmirror')
    results = list(db['shows'].find(status='done'))
    print "Inicializando com %d workers " % NUM_WORKERS
    pool = Pool(processes=NUM_WORKERS)
    pool.map(worker, results)
