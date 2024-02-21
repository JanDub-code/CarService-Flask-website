from flask import render_template,Blueprint,session,request,abort,redirect
from views import models
from functions.sprava_vozidel import pridat_vozidlo,odstranit_vozidlo
from forms import UserSelectForm
from views.models import User, Role, db,Vozidlo



sprava_vozidel = Blueprint("sprava_vozidel", __name__)


@sprava_vozidel.route('/sprava_vozidel')
def spravaVozidel():
    if 'role_id' in session and session['role_id'] in [8, 6, 7, 5]:
        user_id=session['user_id']
        user_role=session['role_id']
        if user_role == 6:
            volba = 2
        elif user_role == 7:
            volba = 1
        else:
            volba = 3

        form = UserSelectForm()
        
        users_with_operations = models.User.query.filter(
            models.User.sluzby.any(models.Sluzba.id_druhu_sluzby == volba)
        ).all()
        form.selected_user.choices = [(user.id, user.username) for user in users_with_operations]


        vozidla = models.Vozidlo.query.filter_by(id_uzivatele=user_id).all()
        operace = models.Sluzba.query.filter(models.Sluzba.id_druhu_sluzby==volba).all()
    elif 'role_id' in session and session['role_id'] in [1]:
        user_id=session['user_id']
        user_role=session['role_id']
        if user_role == 6:
            volba = 2
        elif user_role == 7:
            volba = 1
        else:
            volba = 3

        form = UserSelectForm()
        
        users_with_operations = models.User.query.filter(
            models.User.sluzby.any(models.Sluzba.id_druhu_sluzby == volba)
        ).all()
        form.selected_user.choices = [(user.id, user.username) for user in users_with_operations]
        vozidla = models.Vozidlo.query.all()
        operace = models.Sluzba.query.all()

    else:
        abort(403)
    return render_template('sprava_vozidel.jinja',vozidla=vozidla,operace=operace, form=form)

@sprava_vozidel.route('/sprava_vozidel.zmena_vozidla', methods=['GET', 'POST'])
def sprava():
    if 'role_id' in session and session['role_id'] in [8]:
        if request.method == 'POST' and 'pridej_nove_vozidlo' in request.form:
            return pridat_vozidlo()
        elif request.method == 'POST' and 'odstranit_vozidlo' in request.form:
            return odstranit_vozidlo()
        else:
            return render_template('sprava_vozidel.jinja')
    elif 'role_id' in session and session['role_id'] in [1]:
        if request.method == 'POST' and 'pridej_nove_vozidlo' in request.form:
            nazev = request.form['nazev']
            spz = request.form['spz']
            uzivatel=request.form['uzivatel']
            vozidlo = Vozidlo(id_uzivatele =uzivatel,nazev_vozidla=nazev,spz=spz)

            db.session.add(vozidlo)
            db.session.commit()


            return redirect('/sprava_vozidel')
        elif request.method == 'POST' and 'odstranit_vozidlo' in request.form:
            nazev_odstranit = request.form['nazev_odstranit']
            spz= request.form['spz_od']
            vozidlo = Vozidlo.query.filter_by(spz=spz, nazev_vozidla=nazev_odstranit).first()

            if vozidlo:
                db.session.delete(vozidlo)
                db.session.commit()
            
            return redirect('/sprava_vozidel')
        else:
            return render_template('sprava_vozidel.jinja')
    else:
        abort(403)
    
@sprava_vozidel.route('/sprava_vozidel.zobrazeni', methods=['POST'])
def spravaZobrazeni():
    if 'role_id' in session and session['role_id'] in [1, 6, 7, 5]:

        user_id = session['user_id']
        user_role = session['role_id']
        
        form = UserSelectForm()
        
        # Pokud je vybraný uživatel k dispozici v request.form, použijeme jeho ID
        selected_user_id = request.form.get('selected_user', user_id)

        if user_role == 6:
            volba = 2
        elif user_role == 7:
            volba = 1
        else:
            volba = 3
        
        operace = models.Sluzba.query.filter(models.Sluzba.id_druhu_sluzby == volba).all()

        users_with_operations = models.User.query.filter(
            models.User.sluzby.any(models.Sluzba.id_druhu_sluzby == volba)
        ).all()
        
        form.selected_user.choices = [(user.id, user.username) for user in users_with_operations]

        operace_select = models.Sluzba.query.filter(
            (models.Sluzba.id_druhu_sluzby == volba) &
            (models.Sluzba.id_uzivatele == selected_user_id)
        ).all()
    else:
        abort(403)

    return render_template('sprava_vozidel.jinja', operace=operace, form=form, operace_select=operace_select)


@sprava_vozidel.route('/sprava_vozidel/zmena_stavu', methods=['POST'])
def zmena_stavu():
    if 'role_id' in session and session['role_id'] in [1, 6, 7, 5]:
        form = UserSelectForm()

        id_sluzby = request.form.get('id_sluzby')
        novy_stav = request.form.get('novy_stav')
        
        if id_sluzby and novy_stav in ['neprovedeno', 'provedeno', 'v_procesu']:
            operace = models.Sluzba.query.get(id_sluzby)
            operace.stav = novy_stav
            db.session.commit()

            user_id = session['user_id']
            user_role = session['role_id']
            form = UserSelectForm()
        
            
            selected_user_id = request.form.get('selected_user', user_id)

            if user_role == 6:
                volba = 2
            elif user_role == 7:
                volba = 1
            else:
                volba = 3
            
            operace = models.Sluzba.query.filter(models.Sluzba.id_druhu_sluzby == volba).all()

            users_with_operations = models.User.query.filter(
                models.User.sluzby.any(models.Sluzba.id_druhu_sluzby == volba)
            ).all()
            
            form.selected_user.choices = [(user.id, user.username) for user in users_with_operations]

            operace_select = models.Sluzba.query.filter(
                (models.Sluzba.id_druhu_sluzby == volba) &
                (models.Sluzba.id_uzivatele == selected_user_id)
            ).all()
        
        
        
            print('Stav byl úspěšně změněn.', 'success')
            return render_template('sprava_vozidel.jinja', operace=operace, form=form, operace_select=operace_select)

        print(novy_stav,id_sluzby)
        print('Chyba při změně stavu.', 'danger')
    else:
        abort(403)
    return render_template('sprava_vozidel.jinja', operace=operace, form=form, operace_select=operace_select)

