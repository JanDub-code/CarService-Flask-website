from flask import render_template,Blueprint,session,request
from views import models
from functions.sprava_vozidel import pridat_vozidlo,odstranit_vozidlo
from forms import UserSelectForm
from views.models import User, Role, db

zpravy_statistiky = Blueprint("zpravy_statistiky", __name__)


@zpravy_statistiky.route('/statistiky')
def statistiky():
    pocty_operaci = {
        'neprovedeno': {},
        'v_procesu': {},
        'provedeno': {}
    }

    druhy_sluzeb = models.DruhSluzby.query.all()

    for druh_sluzby in druhy_sluzeb:
        id_druhu_sluzby = druh_sluzby.id_druhu_sluzby
        nazev_druhu_sluzby = druh_sluzby.nazev

        pocty_operaci['neprovedeno'][nazev_druhu_sluzby] = models.Sluzba.query.filter_by(stav='neprovedeno', id_druhu_sluzby=id_druhu_sluzby).count()
        pocty_operaci['v_procesu'][nazev_druhu_sluzby] = models.Sluzba.query.filter_by(stav='v_procesu', id_druhu_sluzby=id_druhu_sluzby).count()
        pocty_operaci['provedeno'][nazev_druhu_sluzby] = models.Sluzba.query.filter_by(stav='provedeno', id_druhu_sluzby=id_druhu_sluzby).count()

    return render_template('statistiky.jinja',pocty_operaci=pocty_operaci)

@zpravy_statistiky.route('/statistiky.filtrace', methods=['GET', 'POST'])
def filtruj():
    pocty_operaci = {
        'neprovedeno': {},
        'v_procesu': {},
        'provedeno': {}
    }

    druhy_sluzeb = models.DruhSluzby.query.all()

    for druh_sluzby in druhy_sluzeb:
        id_druhu_sluzby = druh_sluzby.id_druhu_sluzby
        nazev_druhu_sluzby = druh_sluzby.nazev

        pocty_operaci['neprovedeno'][nazev_druhu_sluzby] = models.Sluzba.query.filter_by(stav='neprovedeno', id_druhu_sluzby=id_druhu_sluzby).count()
        pocty_operaci['v_procesu'][nazev_druhu_sluzby] = models.Sluzba.query.filter_by(stav='v_procesu', id_druhu_sluzby=id_druhu_sluzby).count()
        pocty_operaci['provedeno'][nazev_druhu_sluzby] = models.Sluzba.query.filter_by(stav='provedeno', id_druhu_sluzby=id_druhu_sluzby).count()

    user_id = session['user_id']
    user_role = session['role_id']

    zacatek = request.form['vypis_zacatek']
    konec = request.form['vypis_konec']

    print(zacatek,konec)

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

    filtrace = models.Sluzba.query.filter(models.Sluzba.id_druhu_sluzby.in_(volba),
                                         models.Sluzba.datum.between(zacatek, konec)).all()

                                         
    return render_template('statistiky.jinja',pocty_operaci=pocty_operaci,filtrace=filtrace)


