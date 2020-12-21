## Instruções

1. Clonar o repositório com `git clone `
1. Instalar dependências com  `pip install -r requirements.txt`
1. Ter uma instância do redis rodando localmente (jeito mais fácil: `docker run -p 6379:6379 -d redis:5`)
1. Rodar as migrações com `python manage.py migrate`
1. Carregar fixtures com `python manage.py loaddata start`
1. Rodar o servidor com `python manage.py runserver`

Essa aplicação também está rodando no [Heroku](immuwallet.herokuapp.com).