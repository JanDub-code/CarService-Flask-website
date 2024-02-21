from flask import session,render_template

def logout_user():
    session.pop('user', None)
    return render_template("prihlaseni.jinja")