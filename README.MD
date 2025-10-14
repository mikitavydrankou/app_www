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
Via script
```
chmod +x scripts/run_dev.sh
./scripts/run_dev.sh
```
Or via Docker Compose
```
docker compose -f compose.dev.yml up --build -d
```

## Run Migrations for testing
Via script
```
chmod +x scripts/run_migration.sh
./scripts/run_migration.sh
```
Or via Docker Compose
```
docker compose run django-web python manage.py migrate
```