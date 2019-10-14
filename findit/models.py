from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from findit import db, login_manager
from flask_login import UserMixin

association_table = db.Table('association', db.Model.metadata,
                             db.Column('left_id', db.Integer, db.ForeignKey('technology.id')),
                             db.Column('right_id', db.Integer, db.ForeignKey('user.id'))
                             )


class EmploymentType(db.Model):
    __tablename__ = 'employment'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"EmploymentType('{self.type}')"


class Technology(db.Model):
    __tablename__ = 'technology'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('User', secondary=association_table, back_populates='technologies')

    def __repr__(self):
        return f"Technology('{self.title}')"


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('User', back_populates='city')

    def __repr__(self):
        return f"City('{self.name}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20), unique=True)
    skype = db.Column(db.String(60), unique=True)
    department = db.Column(db.Integer, nullable=False)
    technologies = db.relationship('Technology', secondary=association_table, back_populates='users')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    city = db.relationship('City', back_populates='users')
    password = db.Column(db.String(60), nullable=False)
    vacancies = db.relationship('Vacancy', backref='author', lazy=True)
    description = db.Column(db.Text)
    expectations = db.Column(db.Text)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Vacancy(db.Model):
    __tablename__ = 'vacancy'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Vacancy('{self.title}', '{self.date_posted}')"
