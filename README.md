# expense-tracker

## Overview

Ovo je aplikacija za praćenje troškova. Omogućava kućanstvima ili individualnim korisnicima da praće svoje troškove, planiraju budžet i analiziraju svoje troškove.

Stack:
- FastAPI
- SQLModel
- PostgreSQL
- Docker
- Alembic

## Features

- Višekorisnički sustav (multi-tenant)
- Upravljanje korisnicima
- Upravljanje transakcijama
- Upravljanje kategorijama
- Upravljanje kućanstvima
- Upravljanje valutama
- Generiranje izvještaja


## Docker

Build: `docker compose build`
Run: `docker compose up`

## API dokumentacija

Dokumentacija se nalazi na `http://localhost:8000/docs`.

## Migracija

Događa se koristeći Alembic i automatizirana je tokom docker builda.

Za dodavanje novih migracija, koristi se `docker compose run --rm -w /usr/src/app/migrations backend alembic revision --autogenerate -m "message"`.
Vrijedi napomenuti da se u migracijama mora koristiti SQLModel, a ne SQLAlchemy. [zahtjeva import sqlmodel u početku koja se nalazi u migrations/alembic/versions]
Pri stvaranju novih modela, potrebno je importat model u modul `__init__.py` da bi bio učitan u migracije.

- primjena migracija, koristi se `docker compose run --rm -w /usr/src/app/migrations backend alembic upgrade head`.
- pogledanje trenutnog stanja baze koristi se `docker compose run --rm -w /usr/src/app/migrations backend alembic current`.
- brisanje svih migracija koristi se `docker compose run --rm -w /usr/src/app/migrations backend alembic downgrade base`.
- rollback migracija koristi se `docker compose run --rm -w /usr/src/app/migrations backend alembic downgrade -1`.




