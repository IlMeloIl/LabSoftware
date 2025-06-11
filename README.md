# Usando docker-compose.prod.yml, necesário configurar as variáveis de ambiente

Seu arquivo .env deve estar no mesmo diretório de docker-compose.prod.yml e deve conter o seguinte:

```
SECRET_KEY=secret_key
DEBUG=False ou True

POSTGRES_DB=postgres
POSTGRES_USER=user
POSTGRES_PASSWORD=password
```

Após a configuração do arquivo .env, execute o comando:

```
docker compose -f docker-compose.prod.yml up
```

Vá para localhost:8000 e verifique se a aplicação está funcionando corretamente.

# Criando um superuser

Para criar um superuser, execute o comando:
```
docker exec -it django_app python manage.py createsuperuser
```
e siga os passos fornecidos.

# Conectando ao banco de dados

Para conectar-se ao banco de dados, utilize as credenciais definidas no arquivo .env. <br>
A porta configurada é 5432, como visto em config/settings.py.