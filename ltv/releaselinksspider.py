# -*- coding: utf-8 -*-
import datetime
from bs4 import BeautifulSoup as BS
import requests
import dataset


class ReleaseLinksSpider(object):
    def __init__(self, results=[], db_url=None, verbose=True):
        self.db = dataset.connect(db_url)
        if type(results) is not list:
            results = [results]
        self.results = results
        self.links = []
        self.verbose = verbose

    def work(self):
        for show in self.results:
            self.show = show
            self.__get_links()
            self.__save_links()

    def __get_links(self, pagina=1):
        if self.verbose:
            print "Show id: {id}, Page: {page}".format(id=self.show['show_id'], page=pagina)
        url = 'http://legendas.tv/util/carrega_legendas_busca/id_filme:{num}/page:{page}'.format(
            num=self.show['show_id'],
            page=pagina
        )
        page = requests.get(url, headers={'X-Requested-With': 'XMLHttpRequest'})
        soup = BS(page.content)
        print page.content
        _links = [
            {
                'link': s['href'],
                'show_id':self.show['show_id'],
                'idioma': s.find_parents('div', {'class': 'gallery'})[0].find('img')['title'],
            }
            for s in soup.find_all('a') if s.get('href') and s.get('href', '').startswith('/download')
        ]
        self.links.extend(_links)
        load_more = soup.find_all('a', attrs={'class': 'load_more'})
        if self.verbose:
            print "Adicionando links: ", _links
        if load_more:
            return self.__pega_links(pagina+1)

    def __save_links(self):
        self.db.begin()
        self.show['exists'] = bool(self.links)
        self.show['last_change_time'] = datetime.datetime.now()
        self.show['status'] = 'new'
        self.db['shows'].update(self.show, ['id'])
        for link in self.links:
            print "[{show} Salvando link {link}".format(show=link['show_id'], link=link['link'])
            self.__save_link(link)
        self.db.commit()
        self.links = []

    def __save_link(self, link):
        release = dict(status='new',
                       language=link['idioma'],
                       release_link=link['link'],
                       show_id=self.show['id'],
                       slug='',
                       subtitle_download_link='',
                       last_change_time=datetime.datetime.now(),
                       filename='')
        self.db['releases'].insert(release, ensure=False)


def worker(args):
    results, db_url = args
    m = ReleaseLinksSpider(results, db_url)
    try:
        m.work()
    except Exception, ex:
        print "Exception {ex} ao tentar baixar {results}".format(ex=ex, results=results)
