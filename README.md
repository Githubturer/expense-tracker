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
- Autentifikacija i autorizacija [JWT]
- Slanje emailova za verifikaciju
- Upravljanje korisnicima
- Upravljanje transakcijama
- Upravljanje kategorijama
- Upravljanje kućanstvima [Nije skroz implementirano]
- Upravljanje valutama [TODO]
- Generiranje izvještaja


## Docker

Build: `docker compose build`
Run: `docker compose up`

## API dokumentacija

Dokumentacija se nalazi na `http://localhost:8000/docs`.

## Migracija

Događa se koristeći Alembic i automatizirana je tokom docker builda.

Za dodavanje novih migracija, koristi se `docker compose run --rm backend alembic revision --autogenerate -m "message"`.
Vrijedi napomenuti da se u migracijama mora koristiti SQLModel, a ne SQLAlchemy. [zahtjeva import sqlmodel u početku koja se nalazi u migrations/alembic/versions]
Pri stvaranju novih modela, potrebno je importat model u modul `__init__.py` da bi bio učitan u migracije.

- primjena migracija, koristi se `docker compose run --rm  backend alembic upgrade head`.
- pogledanje trenutnog stanja baze koristi se `docker compose run --rm backend alembic current`.
- brisanje svih migracija koristi se `docker compose run --rm backend alembic downgrade base`.
- rollback migracija koristi se `docker compose run --rm backend alembic downgrade -1`.

## MOCK EMAIL SERVIS

Za testiranje emaila, koristi se mock email servis.

Nalazi se na `http://localhost:8025/`

Sluzi za registraciju korisnika, te slanje emailova za verifikaciju. 
Zaboravljene sifre, ponovno slanje emailova za verifikaciju.

## PGADMIN

Nalazi se na `http://localhost:8080/`

Koristi se za gledanje stanja baze podataka.
pri ulasku se logira sa:
- email: `admin@example.com`
- password: `admin`

registriranje novog servera:
- Host: `db`
- Username: `postgres`
- Password: `somepassword`

## Login

Populirani su useri za testiranje.

for i in range(1, 11):
    - email: `admin{i}@email.com`
    - password: `admin{i}`

## TODO Features

- Git hooks za linting i formatiranje
- Testiranje
- CI/CD pipeline
- OCR za unos transakcija
- Kategorizacija transakcija pri unošenju [Automatizacija kroz LLM za prototipiranje]
- Postavljanje potpunog multitenant sustava [zasad nema izvjestaja za kućanstva, samo za pojedince]
- Postavljanje buđžeta
- Postavljanje valuta i konverzija valuta
- Typechecking
- .toml config file
- global exception handler

Ali dosta o tome. Više u interviewu :D




