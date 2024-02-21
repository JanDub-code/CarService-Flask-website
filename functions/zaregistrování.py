from flask import render_template, request, flash,redirect
from views.models import User, db
from werkzeug.security import generate_password_hash

def registrace():
    if request.method == 'POST':
        username = request.form.get('jmeno')
        email = request.form.get('email')
        telefon = request.form.get('telefon')
        password = request.form.get('heslo')
    
        existing_user = User.query.filter((User.email == email) | (User.phone == telefon)).first()
        if existing_user:
            flash("Email nebo telefonní číslo již existují.")
            return redirect('/registrace')
        elif username == "" or email == "" or telefon == "" or password == "":
            flash("Vyplňte všechna pole.")
            return redirect('/registrace')
        elif len(telefon) != 9:
            flash("Telefonní číslo musí mít 9 číslic.")
            return redirect('/registrace')
        elif (email.find("@") == -1) or (email.find(".") == -1):
            flash("Email musí obsahovat znak @ a .")
            return redirect('/registrace')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, email=email, phone=telefon, password=hashed_password, role_id=8)
            db.session.add(new_user)
            db.session.commit()
            flash("Registrace proběhla úspěšně.")
            #return render_template('prihlaseni.jinja')
            return redirect('/')
    