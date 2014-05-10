# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS
import datetime
import dataset
import requests


class Extractor(object):

    def __init__(self):
        self.db = dataset.connect('postgresql+psycopg2://postgres@10.0.0.101/legendastvmirror')
        self.shows = self.db['shows'].find(status="new")


    def work(self):
        for show in self.shows:
            # Travando o status do show, proteção em caso de falha
            show['status'] = 'extracting'
            show['last_change_time'] = datetime.datetime.now()
            self.db['shows'].update(show, ['id'], ensure=False)
            print "Novo show."
            self.get_download_link(show)

            # Atualizando o status do show, para o gordo consumir
            show['last_change_time'] = datetime.datetime.now()
            show['status'] = 'done'
            self.db['shows'].update(show, ['id'], ensure=False)


    def get_download_link(self, show):
        # Obtendo todas as releases do show
        releases = self.db['releases'].find(id = show['id'])
        for release in releases:
            html = requests.get("http://legendas.tv" + release['release_link'])
            soup = BS(html.content)
            button = soup.find('button', {"class": "icon_arrow"})
            raw_download_link = button['onclick']
            download_link = raw_download_link.split("'")[1]
            print "Obtendo link para " + release['release_link']

            # Altera e salva o release com o novo link para download
            release['subtitle_download_link'] = download_link
            release['last_change_time'] = datetime.datetime.now()
            release['status'] = 'extracted'
            self.db['releases'].update(release, ['id'], ensure=False)

if __name__ == "__main__":
    a = Extractor()
    a.work()
