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
    user_id = db.Column(db.Integer, nullable=False)
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
    def getTasks(user_id):
        return Todo.query.order_by(Todo.date_created).filter_by(is_deleted=0, user_id=user_id).all()

class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_deleted = db.Column(db.Integer, default=0)

    def __repr__ (self):
        return '<User %r>' % self.id

    def update(self):
        db.session.commit()

    def delete(self):
        self.is_deleted = 1
        self.update()

    def save(self):
        # first check if user already exists
        user = User.query.filter_by(email=self.email).first()
        if user is None:
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False

    # implement getUsers() method
    @staticmethod
    def getUsers():
        return User.query.order_by(User.id).filter_by(is_deleted=0).all()

    @staticmethod
    def getUserByEmail(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def getUserByEmailAndPassword(email, password):
        return User.query.filter_by(email=email, password=password).first()

    @staticmethod
    def getUserById(id):
        return User.query.filter_by(id=id).first()