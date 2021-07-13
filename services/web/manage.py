from flask.cli import FlaskGroup

from project.app import app
from project import models


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    models.db.drop_all()
    models.db.create_all()
    models.db.session.commit()


@cli.command('seed_db')
def seed_data():
    models.db.session.add(models.User(username='admin-user', password='pass', is_admin=True, created='2021-08-08'))
    models.db.session.commit()


if __name__ == "__main__":
    cli()
