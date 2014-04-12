# -*- coding: utf-8 -*-
# Exemplo: http://legendas.tv/util/carrega_legendas_busca/id_filme:50000
# 1 - Verificar se tem conteúdo
# 1.1 - Se tiver, ele coloca as urls da página na fila
# "O magro põe na fila, o gordo come"

from bs4 import BeautifulSoup as BS
import requests
import couchdb

class Magro(object):

    def __init__(self, *args, **kwargs):
        self.ids = kwargs['ids']
        server = couchdb.Server(url='http://localhost:5984')
        self.db = server['legendastvurls']

    def work(self, *args, **kwargs):
        for id in self.ids:
            self.id = id
            self.__pega_links()
            self.__salva_links()

    def __pega_links(self, pagina=1, links=[]):
        page = requests.get('http://legendas.tv/util/carrega_legendas_busca/id_filme:{num}/page:{page}'.format(num=self.id,page=pagina))
        soup = BS(page.content)
        links.extend([s['href'] for s in soup.find_all('a') if s.get('href') and s['href'].startswith('/download')])
        load_more = soup.find_all('a', attrs={'class': 'load_more'})
        if load_more:
            return self.__pega_links(pagina+1, links)
        else:
            self.links = links

    def __salva_links(self):
        for link in self.links:
            self.__salva_link(link)

    def __salva_link(self, link):
        self.db.save({'_id': link, 'work_date': None, 'finished_date': None, 'show_id': self.id})
