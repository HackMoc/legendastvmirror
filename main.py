#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import dataset
import datetime
import itertools
import multiprocessing
from ltv import releaselinksspider
from ltv import setupdb
from ltv import subtitlesdownloader
from ltv import id_generator


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate-ids', help='Gera os ids dos filmes (primeiro passo)', default=30000, type=int)
    parser.add_argument('--dbhost', help='Hostname/IP do servidor de banco de dados', default='localhost')
    parser.add_argument('--get-release-links', help='Executa o módulo "releaselinksspider"', action='store_true')
    parser.add_argument('--download-subtitles', help='Baixa as legendas após obter os links de release', action='store_true')
    parser.add_argument('--setupdb', help='Inicializa o banco de dados', action='store_true')
    parser.add_argument('--workers', help='Hostname/IP do servidor de banco de dados', default=10, type=int)
    args = parser.parse_args()

    db_url = 'postgresql+psycopg2://postgres@{db_host}/legendastvmirror'.format(db_host=args.dbhost)

    if args.setupdb:
        print 'Inicializando banco de dados...'
        setupdb.setup(db_url)

    if args.get_release_links:
        db = dataset.connect(db_url)
        _30diasatras = datetime.datetime.now() - datetime.timedelta(30)
        results = list(db['shows'].find(exists=None))
        print "Inicializando com %d worker(s)..." % args.workers
        if args.workers > 1:
            pool = multiprocessing.Pool(processes=args.workers)
            # Necessário para passar o parâmetro 'db_url' para todas as threads
            pool.map(releaselinksspider.worker, itertools.izip(results, itertools.repeat(db_url)))
        else:
            releaselinksspider.worker(args=(results, db_url))
        print "Finalizado."
        exit(0)
    if args.download_subtitles:
        subtitlesdownloader.run()
    if args.generate_ids:
        id_generator.run(args.generate_ids)
