SAM Buildout
============

Sistema operacional
-------------------

Todos os serviços são desenvolvidos sob o sistema operacional **Debian 6 (Squeeze) 64 bits**  e seu funcionamento só
é garantido em tal sistema operacional.

Dependências do sistema
-----------------------

Para o funcionamento do serviço, é necessário que os seguintes pacotes estejam instalados
no sistema: ``python-dev, python-setuptools, python-webunit, python-docutils, libxml2-dev, libxslt1-dev,
python-profiler, unzip``.

Durante a instalação do serviço, ao executar o comando ``make``, todas essas dependências serão devidamente instaladas.


Arquitetura
-----------

Como pode ser visto no pacote **nsi.sam** o sistema consiste em um **webservice RESTful**
hostiado por padrão na **porta 8888** na url **http://localhost/**.

O serviço possui **autenticação HTTP básica** onde os usuários com acesso permitido
ficam em um banco SQLite e todos os parâmetros devem ser passados no coro da requisição
formatos como **json**. Ele é composto por 4 verbos http:

GET
    É o verbo responsável pela recuperação de chaves adicionadas no sistema.
    Ele recebe um parâmetro **key**, que é a chave do dado que foi armazenado
    pelo verbo **PUT**. Se a chave existir, ele retornará um dicionário com os metadados
    criados automaticamente pelo serviço e o dado armazenado anteriormente na chave "data". Caso a chave
    não exista, será retornado um erro **http 404**, informando que a chave não foi encontrada.


POST
    É o verbo responsável pela adição de chaves no sistema de armazenamento.
    Ele recebe um parâmetro **value** no corpo da request que corresponderá ao
    dado que será inserido no banco de dados. Retornará para o usuário uma
    **key**, que é a chave que deverá ser usada para recuperar o valor armazenado. E
    uma chave **checksum**, que contém o **hash sha1** gerado com a **representação em json
    do dicionário** que será recuperado ao usar o verbo **GET**. Também há uma chave **history** onde ficam
    armazenados data, hora e o nome do usuário que realizou mudanças no registro.

PUT
    É o verbo responsável pela atualização do valor armazenado em uma determinada chave.
    Este deve receber dois parâmetros: **key** (chave para o valor) e **value** (valor atualizado).
    Caso a chave fornecida exista e o valor seja atualizado com sucesso, o servidor retornará
    um parâmetro **key** confirmando a chave atualizada e o checksum atualizado para a chave,
    caso contráro o servidor apresentará um erro **http 404, informando key not found**.

DELETE
    Deleta uma chave do sistema de armazenamento. Recebe como parâmetra uma **key** (chave) a ser
    deletada. Se ela existir e a deleção ocorrer com sucesso, retorna uma chave **deleted** com valor
    verdadeiro. Se a chave não existir ele simplesmente retorna a mesma chave com valor falso.


Armazenamento específico de arquivos
------------------------------------

O serviço tratará como arquivo os registros que possuírem estrutura de dicionario com as chaves
"file" e "filename". O conteúdo da chave "file" (o arquivo propriamente dito) será salvo no sistema
de arquivos e seu **hash sha1** será calculado e armazenado no banco de dados, dentro da chave "checksum".

É possível acessar o conteúdo da chave "file" através do navegador, pela url http://usuario:senha@localhost:8888/file/chave,
onde "chave" corresponde à chave onde o conteúdo foi armazenado.


Bibliotecas
-----------

Cyclone
    Cyclone é um fork do Tornado, um webserver criado originalmente pelo
    FriendFeed, que foi comprado pelo Facebook mais tarde e teve seu código
    aberto. É baseado no Twisted e tem suporte a bancos noSQL, como MongoDB e
    Redis, XMLRPC e JsonRPC, além de um servidor HTTP assíncrono.

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

Basta executar: ``bin/samctl start`` e o serviço estará funcionando perfeitamente.
Para adicionar usuário que terão permissão de acesso ao serviço utilizar:
``python bin/add-user.py usuario senha``. E para remover:
``python bin/del-user.py usuario``.


Rodando os testes
-----------------

Para rodar os testes com o serviço parado, basta rodar: ``make test``.
Caso o serviço estejam rodando e não for interessante pará-lo para testá-lo,
basta utilizar o exetucável disponível em ``utils/sam_test``. Ele recebe como parâmetro,
em ordem, host, porta, usuário e senha do SAM que será testado e realiza **testes básicos**
nele.


Consumindo o serviço manualmente (usando Python)
------------------------------------------------

Com uma biblioteca qualquer capaz de realizar requisições HTTP basta enviar uma
requisição usando o verbo desejado e passar os parâmetros necessários em formato
json no corpo da requisição. Não esquecendo da autenticação http simples.

O resultado será retornando no corpo da requisição, codificado em json.
