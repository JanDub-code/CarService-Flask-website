from flask import render_template, Blueprint, session, abort, request
from views.models import User, Role, db


sprava_uzivatele = Blueprint("sprava_uzivatele", __name__)

@sprava_uzivatele.route('/sprava_uzivatelu')
def sprava_uzivatelu():
    if 'role_id' in session and session['role_id'] == 1:
        users = (
            User.query
            .join(Role, User.role_id == Role.id)
            .add_columns(User.id, User.username, Role.name.label('role_name')) 
            .all())
    else:
        abort(403)
    return render_template('sprava_uzivatelu.jinja', users=users)



@sprava_uzivatele.route('/sprava_uzivatelu.uprava_uzivatele', methods=['POST'])
def update():
    if 'role_id' in session and session['role_id'] == 1:
        
        users = (
            User.query
            .join(Role, User.role_id == Role.id)
            .add_columns(User.id, User.username, User.role_id, Role.name.label('role_name')) 
            .all()  
        )   

        users = User.query.join(Role, User.role_id == Role.id).all()
        roles = request.form.getlist('roles[]')

        for user, role_id in zip(users, roles):
            user.role_id = role_id
            db.session.commit()

        users = (
                User.query
                .join(Role, User.role_id == Role.id)
                .add_columns(User.id, User.username, Role.name.label('role_name')) 
                .all()
            )
    else:
        abort(403)
    

    return render_template("sprava_uzivatelu.jinja",users=users)
