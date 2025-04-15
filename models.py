from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta, datetime

db = SQLAlchemy()

class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    course = db.Column(db.Text)
    author = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref='discussion', cascade="all, delete-orphan", lazy=True)
    up_votes = db.Column(db.Integer, default = 0)

    def __repr__(self) -> str:
        string = f"ID: {self.id}, Title: {self.title}, Content: {self.content}, Created_At: {self.created_at}, Course: {self.course}, Author: {self.author}"
        return string
    
    def serialize(self):
        return {"id": self.id,\
                "title": self.title,\
                "content": self.content,\
                "course": self.course,\
                "author": self.author,\
                "up_votes": self.up_votes,\
                "created_at": self.created_at}

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    rating = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref='review', cascade="all, delete-orphan", lazy=True)
    major = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        string = f"ID: {self.id}, Title: {self.title}, Content: {self.content}, Created_At: {self.created_at}, Rating: {self.rating}, Author: {self.author}, Comments: {self.comments}, Major: {self.major}"
        return string
    
    def serialize(self):
        return {"id": self.id,\
                "title": self.title,\
                "content": self.content,\
                "rating": self.rating,\
                "author": self.author,\
                "created_at": self.created_at, \
                "major": self.major}

class Comment(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     discussion_id = db.Column(db.Integer, db.ForeignKey('discussion.id'))
     review_id = db.Column(db.Integer, db.ForeignKey('review.id'))
     content = db.Column(db.Text, nullable=False)
     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
     author = db.Column(db.Text, nullable=False)

# Define the User model
# with columns: ID (primary key), username, password, date_added
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(30), unique=True, nullable=False)  # Unique username
    password = db.Column(db.String(150), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now())      

    # __repr__ returns a String representation of the Users class when
    # we print out an object of type Users
    def __repr__(self) -> str:
        return f"ID: {self.id}, Username: {self.name}, Password: {self.password}"