# HH-scarper

HH-scarper allows you to send a request to the Headhunter API for further aggregating information on key skills and used words in vacancies.
All fetched data are displaying by graphs and lists and can be downloaded.
This app can be found here: [HH-scarper](https://hhscarper.herokuapp.com)

![HH-scarper](materials/hhscarper.gif)

## Tests and  linter status

[![hh-scarper-check.yml](https://github.com/RamiGaggi/hh-scarper/actions/workflows/hh-scarper-check.yml/badge.svg)](https://github.com/RamiGaggi/hh-scarper/actions/workflows/hh-scarper-check.yml)

## Codeclimate

[![Maintainability](https://api.codeclimate.com/v1/badges/2fafd3f436b22a0eaf9b/maintainability)](https://codeclimate.com/github/RamiGaggi/hh-scarper/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/2fafd3f436b22a0eaf9b/test_coverage)](https://codeclimate.com/github/RamiGaggi/hh-scarper/test_coverage)

## Prerequisites

- make
- poetry

## Install

1) Clone repository ```git clone https://github.com/RamiGaggi/hh-scarper.git```
2) Go to working directory ```cd hh-scarper```
3) Set up environment variables in  *.env*
   - DB_ENGINE (defaults to SQLite), set another db engine this way, for example postgres `postgres://user:password@host:port/db_name`
   - SECRET_KEY, for generation you can use `make secret-key`
   - CELERY_BROKER_URL, CELERY_RESULT_BACKEND better use Redis for example `redis://localhost:6379`
4) Install dependencies ```make install```
5) Сomplete setup `make setup`

## Run development server

### Poetry

1) ```make runserver```
2) ```redis-server```
3) ```make celery-worker```
4) Optional, for Celery monitoring: ```make flower```
