from TAAS import db
from datetime import date
from datetime import datetime


class Statistics(db.Model):
    __bind_key__ = 'statistics'
    id = db.Column(db.Integer, primary_key=True)
    mname = db.Column(db.String(30))
    demand = db.Column(db.Integer)
    rvnu = db.Column(db.Integer)
    feedback = db.Column(db.Float)
    fuel = db.Column(db.Integer) 
    mntnc = db.Column(db.Integer)


class CModel(db.Model):
    __bind_key__ = 'cmodel'
    mno = db.Column(db.Integer, primary_key=True)
    mname = db.Column(db.String(20), nullable=False)
    accar = db.Column(db.Integer)
    naccar = db.Column(db.Integer)
    feedback = db.Column(db.Float, default=5.0)
    rent_h = db.Column(db.Integer)
    rent_k = db.Column(db.Integer)


class Car(db.Model):
    __bind_key__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.Integer)
    mname = db.Column(db.String(20))
    pdate = db.Column(db.DateTime, default=date.today())
    kms = db.Column(db.Integer)
    ac = db.Column(db.Boolean)
    avl = db.Column(db.Integer)
    fuel = db.Column(db.Integer)

    def repr(self) -> str:
        return f"{self.carno} - {self.model}"


class Administrator(db.Model):
    __bind_key__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rvnu = db.Column(db.Integer)


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    uname = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    jdate = db.Column(db.DateTime, default=date.today())
    bcar = db.Column(db.Integer, default=0)
    pjrny = db.Column(db.Integer)

    def repr(self) -> str:
        return f"{self.name} - {self.password} - {self.date}"


class Booking(db.Model):
    __bind_key__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    cust = db.Column(db.Integer)
    car = db.Column(db.Integer)
    cmodel = db.Column(db.String(30))
    advance = db.Column(db.Integer)
    bdate = db.Column(db.DateTime, default=datetime.utcnow())
    ereturn = db.Column(db.DateTime)


class Journey(db.Model):
    __bind_key__ = 'journey'
    id = db.Column(db.Integer, primary_key=True)
    cust = db.Column(db.Integer)
    car = db.Column(db.Integer)
    cmodel = db.Column(db.String(30))
    bdate = db.Column(db.DateTime, default=datetime.utcnow())
    rdate = db.Column(db.DateTime, default=datetime.utcnow())
    kms = db.Column(db.Integer)
    fare = db.Column(db.Integer)