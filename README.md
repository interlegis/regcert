# regcert
Sistema de Registros de Certificados


## Instalação

A instalação do Regcert pode ser feita de duas formas, usando o [módulo Puppet do projeto](https://github.com/interlegis/puppet-regcert) que instala e prepara tudo que é necessário (python requirements, nginx, postgresql, etc) para produção, ou clonando o repositório e instalando cada uma das dependências.

*A segunda forma é recomendada apenas para desenvolvimento.*

### Desenvolvimento

```
# apt-get install git python-dev python-pip
```

Clonando o repositório:
```
$ git clone git@github.com:interlegis/regcert
```

Criando um ambiente virtual com virtualenvwrapper ([como instalar](http://virtualenvwrapper.readthedocs.org/)) para instalar as dependências python isoladamente:
```
$ mkvirtualenv regcert
```

Instalando as dependências python:
```
$ pip install -r requirements/dev-requirements.txt
```

Criando o arquivo de configurações *.env*:
```
$ vim src/.env
```
Exemplo:
```
DEBUG=True
SECRET_KEY=STRING_QUALQUER
ALLOWED_HOSTS=127.0.0.1,127.0.0.2
DATABASE_URL=postgresql://user:secret@localhost/database_name
```

### Executando

Rodando migrações:
```
$ ./src/manage.py migrate
```

Executando servidor de desenvolvimento:
```
$ ./src/manage.py runserver
```

Pronto, o regcert deverá estar disponível em http://localhost:8000.
