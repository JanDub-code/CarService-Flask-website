from flask import render_template,Blueprint
from functions import zaregistrování

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route('/registrace')
def registration():
    return render_template('registrace.jinja')


@auth_bp.route('/registrace', methods=['POST'])
def reg():
    return zaregistrování.registrace()

@auth_bp.route('/mujweb.jinja')
def uvod():
    return render_template('mujweb.jinja')



