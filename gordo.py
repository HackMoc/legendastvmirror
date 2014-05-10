# -*- coding: utf-8 -*-
import dataset
import datetime
import os
import requests
import sys


class Gordo(object):

    def __init__(self, base_path, *args, **kwargs)
        self.base_path = base_path
        self.db = dataset.connect('postgresql+psycopg2://postgres@localhost/legendastvmirror')
        self.shows = self.db['shows'].find(status='done')
        self.release = None
        self.show = None

    def work(self, *args, **kwargs):
        for show in self.shows:
            self.show = show
            releases = self.db['release'].find(show_id=show['id'], status='extracted')
            for release in releases:
                self.release = release
                self.__download_subtitle()

    def __download_subtitle(self, *args, **kwargs):
        self.db.begin()
        self.release['status'] = 'downloading'
        self.release['last_change_time'] = datetime.datetime.now()
        self.db['release'].update(self.release, ['id'], ensure=False)
        self.db.commit()
        subtitle = requests.get(url=self.release['subtitle_download_link']).content
        name = '[{language}]{slug}.rar'.format(language=self.release['language'], slug=self.release['slug'])
        filename = os.path.join([self.base_path, self.show['show_name'][0], self.show['show_name'], name])
        with open(filename, 'wb') as arquivo:
            aquivo.write(subtitle)
        self.db.begin()
        self.release['status'] = 'done'
        self.release['last_change_time'] = datetime.datetime.now()
        self.db['release'].update(self.release, ['id'], ensure=False)
        self.commit()


if __name__ == '__main__':
    base_path = sys.argv[1]
    g = Gordo(base_path)
    g.work()
