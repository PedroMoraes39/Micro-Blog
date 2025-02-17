import sqlalchemy
import sqlalchemy.orm

from app import app, db
from app.models import Post, User


@app.shell_context_processor
def make_shell_context():
    return {
        "sa": sqlalchemy,
        "so": sqlalchemy.orm,
        "db": db,
        "User": User,
        "Post": Post,
    }
