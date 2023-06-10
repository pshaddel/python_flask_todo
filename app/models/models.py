from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(200), nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.id

#     def getUsers():
#         return User.query.order_by(User.id).all()

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

class Todo (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Integer, default=0)

    def __repr__ (self):
        return '<Task %r>' % self.id

    def update(self):
        db.session.commit()

    def delete(self):
        self.is_deleted = 1
        self.update()

    def save(self):
        db.session.add(self)
        db.session.commit()

    # implement getTasks() method
    @staticmethod
    def getTasks():
        return Todo.query.order_by(Todo.date_created).filter_by(is_deleted=0).all()
