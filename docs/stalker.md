#	stalker.py

O `Stalker` é uma classe que herda as propriedades de `Magro` e tem como objetivo verificar as [últimas legendas]
(http://legendas.tv/util/carrega_legendas_busca) a cada hora. Comparando-se as entradas da página ao atributo `bookmark`, forma-se a
`release_list`, com os itens que ainda não existem no banco de dados, que será parâmetro de uma chamada ao `extractor`.