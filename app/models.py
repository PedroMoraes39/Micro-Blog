from datetime import datetime
from datetime import timezone
from typing import Optional
import sqlalchemy
import sqlalchemy.orm
from app import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

class User(UserMixin ,db.Model):
    
    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
    
    username: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(64), 
                                                index=True,
                                                unique=True)
    
    email: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(120), 
                                             index=True,
                                             unique=True)
    
    password_hash: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(sqlalchemy.String(256))
    
    last_seen: sqlalchemy.orm.Mapped[Optional[datetime]] = sqlalchemy.orm.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    
    posts: sqlalchemy.orm.WriteOnlyMapped['Post'] = sqlalchemy.orm.relationship(
        back_populates='author')
    
    about_me: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(sqlalchemy.String(140))

    def __repr__(self):
        
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
    
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

class Post(db.Model):
    
    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
    
    body: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(140))
    
    timestamp: sqlalchemy.orm.Mapped[datetime] = sqlalchemy.orm.mapped_column(index=True,
                                                      default=lambda: datetime.now(timezone.utc))
    
    user_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(sqlalchemy.ForeignKey(User.id),
                                               index=True)
    
    author: sqlalchemy.orm.Mapped[User] = sqlalchemy.orm.relationship(back_populates='posts')
    
    def __repr__(self):
        
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
    
    return db.session.get(User, int(id))