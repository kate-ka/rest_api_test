# rest api test


## Technology Stack

- Python 3.7
- Django 2.1.8
- Django REST framework 3.9.4
- PostgreSQL 10

## Installation guideline with pipenv
 - Create your virtual environment with packages: `pipenv shell`
 - Activate virtual environment: `source <path_to_env>/bin/activate`
 - Syncdb: `python manage.py migrate`
 - Run Django server: `python manage.py runserver`
 
 ## Installation guideline with docker
 
 - Install docker : 
    * https://docs.docker.com/install/
    * https://docs.docker.com/compose/install/
 - Run docker-compose `docker-compose up -d`
 
 
 ## Run automated user bot
 - `python app/app/bot/automated_bot.py'

