from app import db, login_manager
from datetime import datetime
from flask_login import (LoginManager, UserMixin, login_required,
                         login_user, current_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Float(), nullable=False)
    employee_id = db.Column(db.Integer(), db.ForeignKey('employees.id'))

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.name)


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer(), primary_key=True)
    second_name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    position_id = db.Column(db.Integer(), db.ForeignKey('positions.id'))
    requests = db.relationship("RequestToDoctor", backref='employee')
    services = db.relationship("Service", backref='employee')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.first_name)


class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    employees = db.relationship('Employee', backref='position')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.name)


class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    requests = db.relationship("RequestToDoctor", backref='status')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.name)


class RequestToDoctor(db.Model):
    __tablename__ = 'requests_to_doctor'
    id = db.Column(db.Integer(), primary_key=True)
    desired_date = db.Column(db.DateTime(), nullable=False)
    result_date = db.Column(db.DateTime())
    created_on = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    employee_id = db.Column(db.Integer(), db.ForeignKey('employees.id'))
    status_id = db.Column(db.Integer(), db.ForeignKey('status.id'))

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.user_id)


# class Wet(db.Model):
#     __tablename__ = 'wets'
#     id = db.Column(db.Integer(), primary_key=True)
#     nickname = db.Column(db.String(255), nullable=False)
#     type_wet = db.Columt(db.String(255), nullable=False)
#     birthday = db.Column(db.Date(), nullable=False)
#     color_id = db.Column(db.Integer(), db.ForeignKey('colors.id'))
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
#
#     def __repr__(self):
#         return "<{}:{}>".format(self.id, self.nickname)
#
#
# class Color(db.Model):
#     __tablename__ = 'colors'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     wets = db.relationship('Wet', backref='color')
#
#     def __repr__(self):
#         return "<{}:{}>".format(self.id, self.name)


# class Category(db.Model):
#     __tablename__ = 'categories'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(255), nullable=False, unique=True)
#     slug = db.Column(db.String(255), nullable=False, unique=True)
#     created_on = db.Column(db.DateTime(), default=datetime.utcnow)
#     posts = db.relationship('Post', backref='category', cascade='all,delete-orphan')
#
#     def __repr__(self):
#         return "<{}:{}>".format(self.id, self.name)
#
#
# post_tags = db.Table('post_tags',
#                      db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
#                      db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
#                      )
#
#
# class Post(db.Model):
#     __tablename__ = 'posts'
#     id = db.Column(db.Integer(), primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     slug = db.Column(db.String(255), nullable=False)
#     content = db.Column(db.Text(), nullable=False)
#     created_on = db.Column(db.DateTime(), default=datetime.utcnow)
#     updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onudate=datetime.utcnow)
#     category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
#
#     def __repr__(self):
#         return "<{}:{}>".format(self.id, self.title[:10])
#
#
# class Tag(db.Model):
#     __tablename__ = 'tags'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     slug = db.Column(db.String(255), nullable=False)
#     created_on = db.Column(db.DateTime(), default=datetime.utcnow)
#     posts = db.relationship('Post', secondary=post_tags, backref='tags')
#
#     def __repr__(self):
#         return "<{}:{}>".format(self.id, self.name)
#
#
# class Feedback(db.Model):
#     __tablename__ = 'feedbacks'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(1000), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     message = db.Column(db.Text(), nullable=False)
#     created_on = db.Column(db.DateTime(), default=datetime.utcnow)
#
#     def __repr__(self):
#         return "<{}:{}>".format(self.id, self.name)
#
#
# class Employee(db.Model):
#     __tablename__ = 'employees'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     designation = db.Column(db.String(255), nullable=False)
#     doj = db.Column(db.Date(), nullable=False)
#
#
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    second_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    requests = db.relationship("RequestToDoctor", backref='user')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

db.create_all()