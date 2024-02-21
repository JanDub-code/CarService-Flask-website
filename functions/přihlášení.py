from flask import render_template, request,flash,session,redirect
from views.models import User
from werkzeug.security import check_password_hash
from forms import PrihlaseniForm

def login():
    form = PrihlaseniForm()

    if request.method == 'POST':
        username_r = form.jmeno.data
        password_r = form.heslo.data
        user = User.query.filter_by(username=username_r).first()
        
        if user and check_password_hash(user.password, password_r):
            session['role_id'] = user.role_id
            session['user_username'] = user.username
            session['user_id']=user.id
            return redirect('/uvod')
        else:
            flash("Přihlášení selhalo. Zkontrolujte jméno a heslo.", 'danger')
            
    
    return render_template('prihlaseni.jinja',form=form)
        
        



    
