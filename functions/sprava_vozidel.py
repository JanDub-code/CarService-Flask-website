from flask import render_template, request,flash,session,redirect
from views.models import User,Vozidlo,db



def pridat_vozidlo():
    if request.method == 'POST' and 'pridej_nove_vozidlo' in request.form:
        nazev = request.form['nazev']
        spz = request.form['spz']
        user_id=session['user_id']
         
        vozidlo = Vozidlo(id_uzivatele =user_id,nazev_vozidla=nazev,spz=spz)
        db.session.add(vozidlo)
        db.session.commit()

        vozidla = Vozidlo.query.filter_by(id_uzivatele=user_id).all()
        return redirect('/sprava_vozidel')
        



def odstranit_vozidlo():
    if request.method == 'POST' and 'odstranit_vozidlo' in request.form:
        nazev_odstranit = request.form['nazev_odstranit']
        user_id = session['user_id']

        vozidlo = Vozidlo.query.filter_by(id_uzivatele=user_id, nazev_vozidla=nazev_odstranit).first()

        if vozidlo:
            db.session.delete(vozidlo)
            db.session.commit()
        vozidla = Vozidlo.query.filter_by(id_uzivatele=user_id).all()
        
    return redirect('/sprava_vozidel')

