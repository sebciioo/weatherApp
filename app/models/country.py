from . import db

"""
    SQLAlchemy database model for the Country table, which stores information about countries.
"""


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False, unique=True)
    short_name = db.Column(db.String(2), nullable=False, unique=True)
