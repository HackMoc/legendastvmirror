# Estruturas de dados

Os diversos *crawlers* no *legendastvmirror* deverão trabalhar sobre as mesmas entidades
presentes no [CouchDB](http://couchdb.apache.org/).

## id_generator

O id_generator é um script indepotente que criará uma lista de ids de shows
para o magro percorrer. Esta lista será salva no CouchDB e terá o seguinte "schema":

## Entidades de um show

Cada show, seja filme ou uma temporada de uma série, no site terá um id Associado.

JSON de Exemplo dos shows:

    "id": primary key,
    "show_id": int,
    "exists": null,
    "show_name": var_char(),
    "status": var_char(),
    "last_change_time": timestamp,

JSON de Exemplo das releases: 

    "id": primmary key,
    "status": small int
    "language": var_char(20)
    "release_link" : var_char()
    "show_id": int chave estrangeira para o `id` do show.
    "slug": var_char(),
    "subtitle_download_link": var_char(),
    "last_change_time" : timestamp,
    "filename": var_char(),

### Atributos

- `show_id`: ID do show extraído pelo **magro**.
- `show_name`: Nome do show obtido pelo **extractor**, apenas na primeira iteração.
- `exists`: Boleano, que definie se o ID pertence a um show válido ou não.
- `episodes`: Lista com todos os episódios do show.
    - `status: Estado atual do episódio`:
        - `new`: Acabou de ser criado pelo **magro**. Preenchendo apenas `status`, `release_link`, `language` e `slug`.
        - `extracting`: O **extractor** começou a trabalhar. Preenchendo o `status` como um *mutex* e atualizando o `Last_change_time`.
        - `extracted`: Foi processado pelo **extractor**. Preenchendo `subtitle_download_link` e `last_change_time`.
        - `downloading`: O **gordo** começou a trabalhar. Atualizando o `status`como um *mutex* e o `Last_change_time`.
        - `Done`: O grodo terminou o trabalho. Atualizando o `status` e o `last_change_time` e finalmente preenchendo o `filename`.
    - `language: Deverá ser a abreviação do idioma ex`: 'pt-br', 'en-us'. Atualizado pelo **magro**.
    - `release_link`: Link para a página que contêm as informações do episódio. Atualizado pelo **magro**. 
Exemplo: "download/52e5425cf17c3/Kuma/Kuma_2012_PROPER_DVDRip_XviD".
    - `slug`: Nome de referência com as informações dos releases. Atualizado pelo **magro**.
Exemplo: "Fargo.S01E02.HDTV.x264-2HD-AFG-FUM-mSD-KILLERS-BS".
    - `subtitle_download_link`: Link para download do arquivo `.rar`das legendas. Atualizado pelo **extractor**.
Exemplo: "/downloadarquivo/535b19c1835ca".
    - `last_change_time`: Último *timestamp* que algum *crawler* fez qualquer alteração no episódio.
    - `filename`: Nome do arquivo salvo pelo **gordo**.
Exemplo: "[pt-br]Fargo.S01E02.HDTV.x264-2HD-AFG-FUM-mSD-KILLERS-BS.rar",
- `status`: Estado atual do show em relação ao extractor, estados:
    - `new`: Criado pelo **Magro** e indica que está pronto para ser trabalhado pelo **extractor**.
    - `extracting`: Indica que o show está sendo extraido nesse momento.
    - `done`: Indica que todos os `subtitle_download_link` foram criados.
- `last_change_time`: Indica quando o show teve sua ultima modificação, **deverá** ser ajustado por todos os crawlers.
