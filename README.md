# Nexora

Sistema independente de gestão de demandas. O backend é Python/Django; HTML e CSS compõem a interface. O banco padrão local é SQLite. Para produção, use PostgreSQL.

## Rodar localmente
Requer Python 3.14 e uv.

    uv sync
    uv run python manage.py migrate
    uv run python manage.py createsuperuser
    uv run python manage.py runserver

Abra http://localhost:8000. O comando createsuperuser pede usuário, e-mail opcional e senha. A conta inicial da administradora deve ser criada no ambiente onde o sistema será usado.

## Configuração
Copie .env.example para .env e defina as variáveis. Nunca publique .env, senhas ou o banco local no GitHub.

No primeiro migrate são cadastradas as empresas Bioflex e Pontual Gráfica. A administradora cria os sistemas e usuários pelo painel /admin/ e vincula cada programador aos sistemas permitidos.

## Vercel
Vercel reconhece projetos Django. Configure DJANGO_SECRET_KEY e DATABASE_URL apontando para PostgreSQL no ambiente de produção. Não use SQLite em produção: o armazenamento local do servidor pode não persistir entre execuções. Após configurar o banco, aplique as migrações com python manage.py migrate.

Ajuste a versão de Python conforme o runtime disponível no provedor. Consulte a documentação do Django e do Vercel antes de publicar.
