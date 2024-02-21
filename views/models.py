from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os

db = SQLAlchemy()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref='users')

class Vozidlo(db.Model):
    id_vozidla = db.Column(db.Integer, primary_key=True)
    id_uzivatele = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='vozidla')
    nazev_vozidla = db.Column(db.String(255), nullable=False)
    spz = db.Column(db.String(10), nullable=False)

class DruhSluzby(db.Model):
    id_druhu_sluzby = db.Column(db.Integer, primary_key=True)
    nazev = db.Column(db.String(255), nullable=False)

class Sluzba(db.Model):
    id_sluzby = db.Column(db.Integer, primary_key=True)
    id_uzivatele = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='sluzby')
    datum = db.Column(db.Date, nullable=False)
    stav = db.Column(db.String(50), nullable=False)
    id_vozidla = db.Column(db.Integer, db.ForeignKey('vozidlo.id_vozidla'), nullable=False)
    vozidlo = db.relationship('Vozidlo', backref='sluzby')
    id_druhu_sluzby = db.Column(db.Integer, db.ForeignKey('druh_sluzby.id_druhu_sluzby'), nullable=False)
    druh_sluzby = db.relationship('DruhSluzby', backref='sluzby')

def is_database_initialized():
    db_file = db.engine.url.database
    return os.path.exists(db_file)

def initialize_db(app):
    db.init_app(app)
    
    if not is_database_initialized():
        with app.app_context():
            db.create_all()

            admin = Role(name="Administrátor boss")
            manager_tech = Role(name="Manažer technické kontroly")
            manager_serv = Role(name="Manažer servisu")
            manager_wreck = Role(name="Manažer likvidace vraků")
            tech_tech = Role(name="Technik technické kontroly")
            tech_serv = Role(name="Technik servisu")
            tech_wreck = Role(name="Technik likvidace")
            customer = Role(name="Zákazník")

            password = "admin"
            admin_password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            admin_user = User(username="admin", password=admin_password_hash, phone="777666457", email="admin@admin.cz", role=admin)

            druh_sluzby_likvidace = DruhSluzby(nazev="Likvidace")
            druh_sluzby_servis = DruhSluzby(nazev="Servis")
            druh_sluzby_technicka_kontrola = DruhSluzby(nazev="Technická kontrola")

            db.session.add(admin)
            db.session.add(manager_tech)
            db.session.add(manager_serv)
            db.session.add(manager_wreck)
            db.session.add(tech_tech)
            db.session.add(tech_serv)
            db.session.add(tech_wreck)
            db.session.add(customer)

            db.session.add(admin_user)

            db.session.add(druh_sluzby_likvidace)
            db.session.add(druh_sluzby_servis)
            db.session.add(druh_sluzby_technicka_kontrola)

            db.session.commit()
