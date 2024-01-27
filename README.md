# Storefront

- This is ecommerce store application built in Python & Django.

## Prerequisits

- Python 3.11.6
- Django 5.0.1
- MySQL
- Docker

## Configuration

### Clone repository and move to app directory

- git clone https://github.com/usamabasharat/store-front.git
- cd store-front

## Enviornmenral Variables

- DB_NAME
- DB_USER
- DB_PASSWORD
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD
- DEFAULT_FROM_EMAIL
- EMAIL_TO

## Prepare & Start Server

- `docker-compose up --build`

## Populate  Database with Sample Data (Optional)

- `docker-compose run web python manage.py seed_db`

## App URL

- http://127.0.0.1:8000//sotre
