# APP-WWW

## Environment Parameters

#### Development (.env.dev)
```
DEBUG=True
DJANGO_LOGLEVEL=debug
```

#### Production (.env.prod)
```
DEBUG=False
DJANGO_LOGLEVEL=info
```

## Dev Server
```
docker compose -f compose.dev.yml up --build -d
```
## Run Migrations for testing
```
docker compose run django-web python manage.py migrate
```
## Create super user
```
docker compose run django-web python manage.py createsuperuser
```