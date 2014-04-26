gordo.py 
========

O gordo é o responsável por obter os links do extractor e baixa-los. O gordo
faz uma consulta na base de dados pelo primeiro show que tiver o atributo
`status` do show como `done`;

O gordo vai percorrer cada um dos links que não foram baixados ou que estão com
o status downloading há mais de 20 minutos dentro do array `episodes` para
baixa-los. Quando começar a baixar um episódio, o gordo vai setar o status como
`downloading` e atualizar o last_change_time com a ultima atualização.
Ao termino do download da legenda, o gordo altera o status do episódio para 'done'
e atualiza novamente o last_change_time.

O timestamp é necessário para termos um `timeout`: gordos que estão baixando
uma legenda há 10 minutos certamente tem algum problema e a legenda precisa ser
baixada novamente;
