cSAM Buildout
============

Arquitetura
-----------

Como pode ser visto no pacote nsi.sam o sistema consiste em um webservice
(xmlrpc) hostiado por padrão na porta 8888 na url
http://usuario:senha@localhost:8888/xmlrpc.

O serviço possui autenticação HTTP básica onde os usuários com acesso permitido
ficam em um banco SQLite. Ele é composto por 3 funções:

set
    É uma função utilizada para guardar qualquer valor dentro do banco de dados
    e retorna a chave para recuperar o mesmo.

    Ao setar uma string o serviço prepara um dicionário, com a data da request,
    o usuário que está fazendo-a, o tamanho dela e a string propriamente dita, e
    guarda ele como string no banco.

update
    Muda o valor em uma determinada chave para outro passado como argumento pela
    função. Detalhe importante: o valor não é o dicionário inteiro! É a string
    que será guardada dentro dele.

delete
    Deleta o valor referente a uma chave, junto com ela.


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

Consumindo o serviço manualmente (usando Python)
Com o serviço devidamente iniciado, abrir um terminal Python. Da biblioteca
*xmlrpclib* importar a classe *Server*.
Criar uma instância da classe *Server*, passando como parâmetro o endereço do
serviço (http://usuario:senha@localhost:8080/xmlrpc). Então todas as funções
poder ser utilizadas: set, update e delete.


Futuro
------

Recentemente a txredisapi foi incluída como parte do Cyclone. Então o código
poderia ser reduzido e simplificado se importasse a biblioteca dele.

Consumindo o serviço manualmente (usando Python)
------------------------------------------------

Com o serviço devidamente inicializado, abrir um terminal Python. Da biblioteca
"xmlrpclib" importar a classe "Server". Criar uma instância da classe server
passando o endereço do servidor (e.g. http://test:test@localhost:8888/xmlrpc).
Agora para guardar dados no SAM é somente chamar o método "set" passando uma
string, caso contrário o código tentará converter o objeto para string usando a
função "str". O UID do dado armazenado será retornado.
Para atualizar o mesmo basta chamar a função "update", passando como parâmetro
o UID e o novo dado, respectivamente. Será retornado True caso o valor seja atu
alizado com sucesso.
Para deletar uma chave, utilizar a função "delete", passando o UID. Caso a seja
seja deletada com sucesso, True será retornado.

