from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = 'deskchampionsknowthesecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer.db'
app.config['SQLALCHEMY_BINDS'] = {'statistics': 'sqlite:///statistics.db', 'cmodel': 'sqlite:///cmodel.db',
                                  'car': 'sqlite:///car.db', 'admin': 'sqlite:///admin.db', 'booking': 'sqlite:///booking.db', 'journey': 'sqlite:///journey.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from TAAS import routes
from TAAS import models