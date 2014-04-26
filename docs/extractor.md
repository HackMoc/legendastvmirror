# extractor.py 

O extractor é responsável por preencher os detalhes de cada episódio para que o 
gordo possa realizar os downloads dos episódios.

O extractor deverá obter os dados de um show a partir do *Couchdb* e 
acessar todos os `release_link` e preencher em cada `episodes` seguindo
os seguintes passos:

1. O extractor deverá mudar o `status` do show e o `last_change_time`.
O `last_change_time` deverá ser atribuido para o timestamp atual. Assim um episódio com mais 
de 10 minutos deverá ser considerado uma falha.
2. O extractor deverá alterar o `status` do show para `extracting`, informando assim
que o processo de extração foi iniciado naquele show.
3. Ao finalizar a extração de um episódio o extractor deverá alterar:
    - `status` do episódio: deverá ser alterado para `extracted`.
    - `subtitle_download_link`: deverá ser preenchido com o link que apontará para o arquivo (.rar).
    - `last_change_time`: deverá ser novamente atualizado o timestamp.
4. Quando todos os episódios estiverem com o `status` igual a `extracted` o extractor deverá 
alterar o `status` do show para `done`, informando assim está pronto para o gordo.
