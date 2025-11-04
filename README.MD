# APP-WWW

## Schema

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            DOCKER COMPOSE SERVICES                            │
└──────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │   Web Browser   │
    │   (Client UI)   │
    └────────┬────────┘
             │ HTTP :8000
             ▼
    ┌─────────────────────────────────────────┐
    │         Django Web Application          │
    │              (django-web)               │
    │─────────────────────────────────────────│
    │  • User Authentication & Registration   │
    │  • PentestRecord Model (PostgreSQL)     │
    │  • PentestForm (Multi-operation)        │
    │  • Home View (History Display)          │
    │  • Templates (Bootstrap-styled)         │
    └───────┬─────────────────────┬───────────┘
            │                     │
            │ SQL                 │ HTTP :8001
            ▼                     ▼
    ┌─────────────────┐   ┌─────────────────────────────┐
    │   PostgreSQL    │   │    Pentest FastAPI Service  │
    │      (db)       │   │       (pentest-api)         │
    │   port: 5432    │   │─────────────────────────────│
    │─────────────────│   │  Endpoints:                 │
    │  • Users        │   │  • POST /ping               │
    │  • Sessions     │   │  • POST /port-scan          │
    │  • Articles     │   │  • POST /dns-lookup         │
    │  • Pentest      │   │  • POST /http-headers       │
    │    Records      │   │  • GET /task/{task_id}      │
    └─────────────────┘   └────────┬────────────────────┘
                                   │
                                   │ Celery Tasks
                                   ▼
                          ┌─────────────────┐
                          │   Redis Broker  │
                          │     (redis)     │
                          │   port: 6379    │
                          │─────────────────│
                          │  • Task Queue   │
                          │  • Results      │
                          └────────┬────────┘
                                   │
                                   │ Pop Tasks
                                   ▼
                    ┌──────────────────────────────────┐
                    │     Celery Worker Service        │
                    │      (pentest-worker)            │
                    │──────────────────────────────────│
                    │  Tasks:                          │
                    │  • ping_host()                   │
                    │    └─> ping3 library             │
                    │  • port_scan()                   │
                    │    └─> nmap subprocess           │
                    │  • dns_lookup()                  │
                    │    └─> nslookup subprocess       │
                    │  • http_headers()                │
                    │    └─> curl subprocess           │
                    └──────────────────────────────────┘

    ┌─────────────────┐
    │     Adminer     │
    │  (adminer-db)   │
    │   port: 8080    │
    │  DB Management  │
    └─────────────────┘
```

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