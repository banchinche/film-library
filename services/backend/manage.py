from flask.cli import FlaskGroup
from app.app import app, db
from app.models.user import User


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("add_user")
def add_user():
    db.session.add(User(username="arima-admin", password='pass', is_admin=True, date='2021-08-08' ))
    db.session.commit()


if __name__ == "__main__":
    cli()