## Instruções

### Sem docker-compose

1. Clonar o repositório com `git clone https://github.com/diego-lima/immuwallet.git`
1. Instalar dependências com  `pip install -r requirements.txt`
1. Ter uma instância do redis rodando localmente (jeito mais fácil: `docker run -p 6379:6379 -d redis:5`)
1. Rodar as migrações com `python manage.py migrate`
1. Carregar fixtures com `python manage.py loaddata start`
1. Rodar o servidor com `python manage.py runserver`

### Com docker-compose

1. subir todos os containers com `docker-compose up`
1. abrir um terminal com `docker-compose run web bash`
1. rodar as migrações e carregar fixtures conforme instruções acima.

Essa aplicação também está rodando no [Heroku](https://immuwallet.herokuapp.com/).