# -*- coding: utf-8 -*-
import datetime
from bs4 import BeautifulSoup as BS
import requests
import dataset

class Magro(object):

    def __init__(self):
        self.db = dataset.connect('postgresql+psycopg2://postgres@localhost/legendastvmirror')
        _30diasatras = datetime.datetime.now() - datetime.timedelta(30)
        self.results = self.db['shows'].find(exists=None)
        self.links = []

    def work(self, *args, **kwargs):
        for show in self.results:
            self.show = show
            self.__pega_links()
            self.__salva_links()

    def __pega_links(self, pagina=1):
        url = 'http://legendas.tv/util/carrega_legendas_busca/id_filme:{num}/page:{page}'.format(num=self.show['show_id'],page=pagina)
        page = requests.get(url, headers={'X-Requested-With':'XMLHttpRequest'})
        soup = BS(page.content)
        _links = [{'link': s['href'],
                  'show_id':self.show['show_id'],
                  'idioma': s.find_parents('div', {'class': 'gallery'})[0].find('img')['title']
                  }
                    for s in soup.find_all('a') if s.get('href') and s['href'].startswith('/download')]
        self.links.extend(_links)
        load_more = soup.find_all('a', attrs={'class': 'load_more'})
        if load_more:
            return self.__pega_links(pagina+1)

    def __salva_links(self):
        self.db.begin()
        self.show['exists'] = bool(self.links)
        self.show['last_change_time'] = datetime.datetime.now()
        self.show['status'] = 'new'
        self.db['shows'].update(self.show, ['id'])
        for link in self.links:
            print "[{show} Salvando link {link}".format(show=link['show_id'], link=link['link'])
            self.__salva_link(link)
        self.db.commit()
        self.links = []

    def __salva_link(self, link):
        release = dict(status='new',
                        language=link['idioma'],
                        release_link=link['link'],
                        show_id=self.show['id'],
                        slug='',
                        subtitle_download_link='',
                        last_change_time=datetime.datetime.now(),
                        filename='')
        self.db['releases'].insert(release, ensure=False)

Magro().work()
