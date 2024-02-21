from flask import render_template,Blueprint,session,request,redirect,url_for,abort
from views import models
from views.models import User, Role, db
from functions.sprava_vozidel import pridat_vozidlo,odstranit_vozidlo
from datetime import datetime



planovani_kalendar = Blueprint("planovani_kalendar", __name__)


@planovani_kalendar.route('/kalendar')
def planovani_A_kalendar():
    if 'role_id' in session and session['role_id'] in [8]:

        user_id=session['user_id']
        druhy_sluzeb = models.DruhSluzby.query.all()
        vozidla = models.Vozidlo.query.filter_by(id_uzivatele=user_id).all()
    elif 'role_id' in session and session['role_id'] in [1]:
        user_id = session['user_id']
        vozidla = models.Vozidlo.query.all()
        druhy_sluzeb = models.DruhSluzby.query.all()
    else:
        abort(403)
    return render_template('kalendar.jinja',vozidla=vozidla,druhy_sluzeb=druhy_sluzeb)

@planovani_kalendar.route('/kalendar.pridani', methods=['GET', 'POST'])
def pridani():
    if 'role_id' in session and session['role_id'] in [8]:
        user_id = session['user_id']
        vozidla = models.Vozidlo.query.filter_by(id_uzivatele=user_id).all()
        druhy_sluzeb = models.DruhSluzby.query.all()

        if request.method == 'POST' and 'pridej' in request.form:
            datum_str = request.form.get('datum')
            datum = datetime.strptime(datum_str, '%Y-%m-%d').date()
            id_sluzby = request.form.get('sluzba')
            id_vozidla = request.form.get('vozidlo')

            print("Datum:", datum)
            print("ID služby:", id_sluzby)
            print("ID vozidla:", id_vozidla)

            if datum and id_sluzby and id_vozidla:
                sluzba = models.Sluzba(
                    id_uzivatele=user_id,
                    datum=datum,
                    stav="neprovedeno",  
                    id_vozidla=id_vozidla,
                    id_druhu_sluzby=id_sluzby
                )

                db.session.add(sluzba)
                db.session.commit()
                print("Služba byla úspěšně přidána.")
                return redirect(url_for('planovani_kalendar.planovani_A_kalendar'))
    elif 'role_id' in session and session['role_id'] in [1]:
        user_id = session['user_id']
        vozidla = models.Vozidlo.query.all()
        druhy_sluzeb = models.DruhSluzby.query.all()

        if request.method == 'POST' and 'pridej' in request.form:
            datum_str = request.form.get('datum')
            datum = datetime.strptime(datum_str, '%Y-%m-%d').date()
            id_sluzby = request.form.get('sluzba')
            id_vozidla = request.form.get('vozidlo')

            print("Datum:", datum)
            print("ID služby:", id_sluzby)
            print("ID vozidla:", id_vozidla)

            if datum and id_sluzby and id_vozidla:
                sluzba = models.Sluzba(
                    id_uzivatele=user_id,
                    datum=datum,
                    stav="neprovedeno",  
                    id_vozidla=id_vozidla,
                    id_druhu_sluzby=id_sluzby
                )

                db.session.add(sluzba)
                db.session.commit()
                print("Služba byla úspěšně přidána.")
                return redirect(url_for('planovani_kalendar.planovani_A_kalendar'))
    else:
        abort(403)

    return render_template('kalendar.jinja',vozidla=vozidla,druhy_sluzeb=druhy_sluzeb)