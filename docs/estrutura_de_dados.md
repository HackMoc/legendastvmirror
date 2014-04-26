# Estrutura de dados

Os diversos crawles no legendastvmirro deverão trabalhar sobre uma mesma entidade
presente no (CouchDB)[http://couchdb.apache.org/] veja abaixo.

Exemplo de Json:

    {
        "show_id": 1,
        "show_name": "name",
        "episodes": [
            {
                "status": "new"
                "language": "flag",
                "release_link" : "download/52e5425cf17c3/Kuma/Kuma_2012_PROPER_DVDRip_XviD"
                "slug": "Fargo.S01E02.HDTV.x264-2HD-AFG-FUM-mSD-KILLERS-BS",
                "subtitle_download_link": "/downloadarquivo/535b19c1835ca",
                "last_change_time" : timestamp,
                "filename": "[pt-br]Fargo.S01E02.HDTV.x264-2HD-AFG-FUM-mSD-KILLERS-BS.rar",
            },
        ],
        "extractor_status": "done",
    }

## Atributos

- show_id: ID do show extraído pelo *magro*.
- show_name: Nome do show obtido pelo *extractor*, apenas na primeira iteração.
- episodes: Lista com todos os episódios do show.
 - status: Estado atual do episódio:
 - new: Acabou de ser criado pelo *magro*. Preenchendo apenas `status`, `release_link`, `language` e `slug`.
 - extracting: O *extractor* começou a trabalhar. Preenchendo o `status` como um *mutex* e atualizando o `Last_change_time`.
 - extracted: Foi processado pelo *extractor*. Preenchendo `subtitle_download_link` e `last_change_time`.
 - downloading: O *gordo* começou a trabalhar. Atualizando o `status`como um *mutex* e o `Last_change_time`.
 - Done: O grodo terminou o trabalho. Atualizando o `status` e o `last_change_time` e finalmente preenchendo o `filename`.

new
working
downloaded
