# Magro

O magro tem como objetivo buscar e listar todas as páginas contendo os links para as páginas de downloads.

## Busca

A busca é realizada a partir da rota /util/carrega_legendas_busca/id_filme:*{inteiro}*/page:*{inteiro}*.
Um range contendo os ids dos filmes é passado para magro, dessa forma, é possível que o magro efetue a busca
em um conjunto de páginas a partir do id_filme especificado. O parâmetro page inicia com o valor 1 e enquanto
a requisição da página possuir algum conteúdo o parâmetro page é incrementado, caso contrário, a busca efetuada na página é dada como concluída.

## Listagem

A partir da busca realizada em cada id_filme o magro informa se aquela página existe ou não, além de informar a última checagem daquela página, caso a página exista é criada uma estrutura de dados
(detalhes da estrutura de dados podem ser vista [aqui](https://github.com/HackMoc/legendastvmirror/blob/master/docs/estrutura_de_dados.md)).
É responsabilidade do magro informar o atributo show_id da estrutura de dados, atributo este que se refere ao id_filme. O magro tem também como
responsabilidade listar todos os links para as páginas de downloads encontradas nas páginas do respectivo show_id.

A cada novo link, o magro insere um novo espisódio com `status` igual a new, informa a linguagem através do atributo `language`,
informa o atributo slug e o link para a página de download da legenda através do atributo release_link.
Ao termino da listagem dos links da página, é alterado o status do show_id para new, informando que aquele show_id está pronto para que o extractor possa trabalhar,
e a última modificação realizada no show_id, para essa alteração é utilizado o campo last_change_time.
