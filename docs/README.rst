SAM Buildout
============

Arquitetura
-----------

Como pode ser visto no pacote nsi.sam o sistema consiste em um webservice RESTful
hostiado por padrão na porta 8888 na url http://localhost:8888/.

O serviço possui autenticação HTTP básica onde os usuários com acesso permitido
ficam em um banco SQLite e todos os parâmetros devem ser passados no coro da requisição
formatos como "json". Ele é composto por 3 verbos http:

PUT
    É o verbo responsável pela adição de chaves no sistema de armazenamento.
    Ele recebe um parâmetro "value" no corpo da request que corresponderá ao
    dado que será inserido no banco de dados. Retornará para o usuário uma
    "key", que é a chave que deverá ser usada para recuperar o valor armazenado. E
    uma chave "checksum", que contém o hash sha1 gerado com a representação em string
    do dicionário que será armazenado no SAM.

POST
    É o verbo responsável pela atualização do valor armazenado em uma determinada chave.
    Este deve receber dois parâmetros: "key" (chave para o valor) e "value" (valor atualizado).
    Caso a chave fornecida exista e o valor seja atualizado com sucesso, o servidor retornará
    um parâmetro "key" confirmando a chave atualizada e o checksum atualizado para a chave,
    caso contráro o servidor apresentará um erro 404 (Key Not Found).

DELETE
    Deleta uma chave do sistema de armazenamento. Recebe como parâmetra uma "key" (chave) a ser
    deletada. Se ela existir e a deleção ocorrer com sucesso, retorna uma chave "deleted" com valor
    verdadeiro. Se a chave não existir ele simplesmente retorna a mesma chave com valor falso.


Bibliotecas
-----------

Cyclone
    Cyclone é um fork do Tornado, um webserver criado originalmente pelo
    FriendFeed, que foi comprado pelo Facebook mais tarde e teve seu código
    aberto. É baseado no Twisted e tem suporte a bancos noSQL, como MongoDB e
    Redis, XMLRPC e JsonRPC, além de um cliente HTTP assíncrono.

txredisapi
    É uma API que promove acesso assíncrono ao banco de dados Redis, feita em
    cima do Twisted.

nsi.sam
    Pacote que define as funções e autenticação do serviço.

Redis (banco de dados)
    Um banco de dados noSQL que promete velocidade em leitura e escrita enormes.

    Possui suporte a listas e conjuntos. A partir da versão 1.4 ele é capaz de
    guardar hashs. A partir da versão 2.0 tem a funcionalidade de clusters e
    auto-replicação. Além de um sistema de mensagens baseado em canais. A versão
    atual em uso é a 2.0.

    O banco fica completamente na memória, como o memcached, e é salvo
    periodicamente no sistema de arquivos usando a política append-only,
    necessitando assim do mínimo possível de IO.


Instalação
----------

Assumindo que o repositório foi devidamente clonado, criar um ambiente virtual
de Python com a versão 2.6. Rodar o “make” dentro do diretório do buildout.
Rezar para que funcione.


Executando
----------

Basta executar: *bin/samctl start* e o serviço estará funcionando perfeitamente.
Para adicionar usuário que terão permissão de acesso ao serviço utilizar:
*python bin/add-user.py usuario senha*. E para remover:
*python bin/del-user.py usuario*.


Rodando os testes
-----------------

Se o SAM estiver rodando, é aconselhável pará-lo: *bin/samctl stop* e então
rodar: *make run_unit_test*.


Futuro
------

Recentemente a txredisapi foi incluída como parte do Cyclone. Então o código
poderia ser reduzido e simplificado se importasse a biblioteca dele.


Consumindo o serviço manualmente (usando Python)
------------------------------------------------

Com uma biblioteca qualquer capaz de realizar requisições HTTP basta enviar uma
requisição usando o verbo desejado e passar os parâmetros necessários em formato
json no corpo da requisição. Não esquecendo da autenticação http simples.

O resultado será retornando como corpo da resposta da requisição.
