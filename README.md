# toolbox-jwt-auth-flask

## To start
1. run `python3 -m venv env` to start a venv.
2. Run `source ./env/bin/activate`
3. Install pip dependencies with `pip install -r ./requirements.txt`

## Add Dependencies
1. Add your new dependency to `requirements.in`
2. Run `pip-compile -o requirements.txt requirements.in --generate-hashes`

## Adding migrations
Migrations is handled by `Flask-Migrate`. To init, run `python manage.py db init`

1. Make changes in model.py, run `docker-compose exec app python manage.py db migrate` to generate the migration file.
2. Run `docker-compose exec app python manage.py db upgrade` to apply your migration(s).

## Run tests
1. Run `docker-compose exec app python -m pytest -s`