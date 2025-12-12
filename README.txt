# run the project:
api dev/production


pip freeze > requirements.txt

# add migration
alembic revision --autogenerate -m "init"

# run migration on database
alembic upgrade head




