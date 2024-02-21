from flask import render_template,Blueprint,session,request,redirect,url_for
from views import models
from views.models import User, Role, db
from functions.sprava_vozidel import pridat_vozidlo,odstranit_vozidlo
from datetime import datetime

stav = Blueprint("stav", __name__)


@stav.route('/stav')
def stav_uzivatele():
    user_id = session['user_id']
    user_role = session['role_id']

    if user_role == 6:
        volba = [2]
    elif user_role == 7 :
        volba = [1]
    elif user_role == 5 :
        volba = [3]
    elif user_role == 3:
        volba = [2]
    elif user_role == 4:
        volba = [1]
    elif user_role == 2:
        volba = [3]
    else:
        volba = [1, 2, 3]

    today = datetime.now().date()

    operace1 = models.Sluzba.query.filter(models.Sluzba.id_druhu_sluzby.in_(volba),
                                          models.Sluzba.datum > today,
                                          models.Sluzba.stav == 'neprovedeno').all()

    operace2 = models.Sluzba.query.filter(models.Sluzba.id_druhu_sluzby.in_(volba),
                                          models.Sluzba.datum <= today,
                                          models.Sluzba.stav == 'neprovedeno').all()

    operace3 = models.Sluzba.query.filter(models.Sluzba.id_druhu_sluzby.in_(volba),
                                          models.Sluzba.stav == 'v_procesu').all()

    operace4 = models.Sluzba.query.filter(models.Sluzba.id_druhu_sluzby.in_(volba),
                                          models.Sluzba.datum < today,
                                          models.Sluzba.stav == 'provedeno').all()

    operace5 = models.Sluzba.query.filter(models.Sluzba.id_druhu_sluzby.in_(volba),
                                          models.Sluzba.datum >= today,
                                          models.Sluzba.stav == 'provedeno').all()

    operace6 = models.Sluzba.query.filter(models.Sluzba.id_uzivatele == user_id).all()

    return render_template('stav.jinja', operace1=operace1, operace2=operace2, operace3=operace3, operace4=operace4, operace5=operace5, operace6=operace6)
