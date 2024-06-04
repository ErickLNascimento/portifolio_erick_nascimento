from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import func

db = SQLAlchemy()


class Duck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mother_id = db.Column(db.Integer, db.ForeignKey('duck.id'), nullable=True)
    mother = db.relationship('Duck', backref=db.backref('children'), remote_side=[id])
    is_sold = db.Column(db.Boolean, default=False)
    price = [50, 70]


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    eligible_for_discount = db.Column(db.Boolean, default=False)


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    client_id = db.Column(db.String, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client')
    ducks = db.relationship('Duck', secondary='sale_duck', backref='sales')
    value = db.Column(db.Integer)


sale_duck = db.Table('sale_duck',
                     db.Column('sale_id', db.Integer, db.ForeignKey('sale.id'), primary_key=True),
                     db.Column('duck_id', db.Integer, db.ForeignKey('duck.id'), primary_key=True),
                     db.Column('duck_name', db.String(50)),
                     db.Column('client_name', db.String(50)),
                     db.Column('value', db.Integer)
                     )
