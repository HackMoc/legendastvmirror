# Estrutura de diretórios

O _gordo_ deve ser executado com o parâmetro `base-path`, que indica o local do
disco onde os arquivos serão salvos:

    gordo.py [opções] --base-path /var/www/files

Os seguintes elementos da entidade de um show são utilizados para formar o nome
dos arquivos:

- `show_name` (_slugified_)
- `language`
- `slug`

Os arquivos serão salvos baseando-se no modelo abaixo:

    <base-path>/<primeira letra do nome>/<slug do nome>/[<código do idioma>]<slug>.rar

Exemplos:

    /var/www/files/f/fargo/[pt-br]Fargo.S01E02.HDTV.x264-2HD-AFG-FUM-mSD-KILLERS-BS.rar
    /var/www/files/t/the-goldbergs/[en-us]The.Goldbergs.2013.S01E18.HDTV.x264-EXCELLENCE-REMARKABLE-AFG.rar
