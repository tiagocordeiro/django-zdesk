# django-zdesk
django-zDesk is a Django simple ticketing system

[![Updates](https://pyup.io/repos/github/tiagocordeiro/django-zdesk/shield.svg)](https://pyup.io/repos/github/tiagocordeiro/django-zdesk/)
[![Python 3](https://pyup.io/repos/github/tiagocordeiro/django-zdesk/python-3-shield.svg)](https://pyup.io/repos/github/tiagocordeiro/django-zdesk/)
[![Python 3.9.7](https://img.shields.io/badge/python-3.9.7-blue.svg)](https://www.python.org/downloads/release/python-397/)
[![Django 3.2.8](https://img.shields.io/badge/django-3.2.8-blue.svg)](https://www.djangoproject.com/download/)
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/tiagocordeiro/django-zdesk/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/tiagocordeiro/django-zdesk/branch/master/graph/badge.svg)](https://codecov.io/gh/tiagocordeiro/django-zdesk)
[![Build Status](https://travis-ci.org/tiagocordeiro/django-zdesk.svg?branch=master)](https://travis-ci.org/tiagocordeiro/django-zdesk)
[![Python application](https://github.com/tiagocordeiro/django-zdesk/workflows/Python%20application/badge.svg)](https://github.com/tiagocordeiro/django-zdesk/actions)

### Como rodar o projeto
* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/tiagocordeiro/django-zdesk.git
cd django-zdesk
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
```

### Configurar administrador
Para cria um usuário administrador
```
python manage.py createsuperuser --username dev --email dev@foo.bar
```

### Configurar grupos de usuários
Cria grupos de usuários: [ `gerente` , `operador` ]
```
python manage.py loaddata core/fixtures/groups.json
```

### Rodar em ambiente de desenvolvimento
Para rodar o projeto localmente
```
python manage.py runserver
```

### Banco de dados para desenvolvimento com Docker
```
docker-compose up -d
```

### Testes, contribuição e dependências de desenvolvimento
Para instalar as dependências de desenvolvimento
```
pip install -r requirements-dev.txt
```

Para rodar os testes
```
python manage.py test -v 2
```

Para rodar os testes com relatório de cobertura.
```
coverage run manage.py test -v 2
coverage html
```

Verificando o `Code style`
```
pycodestyle .
flake8 .
```