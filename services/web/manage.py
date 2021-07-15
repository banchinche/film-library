from operator import mod
from flask.cli import FlaskGroup

from project.app import app
from project import models, seed
# from random import randint, uniform

# from faker import Factory


cli = FlaskGroup(app)

@cli.command('drop_all')
def drop_db():
    models.db.drop_all()

@cli.command('create_db')
def create_db():
    models.db.create_all()
    models.db.session.commit()

@cli.command('create_new_db')
def create_new_db():
    models.db.drop_all()
    models.db.create_all()
    models.db.session.commit()


@cli.command('seed_db')
def seed_db():
    seed.seed(100, 150, 300)
    models.db.session.commit()


if __name__ == "__main__":
    cli()
