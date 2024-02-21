from flask import render_template,Blueprint
from functions import přihlášení

prihlas = Blueprint("prihlas", __name__)

@prihlas.route('/')
def prihlaseni():
    return render_template('prihlaseni.jinja')


@prihlas.route('/', methods=['POST'])
def log():

    return přihlášení.login()

@prihlas.route('/uvod')
def uvod():
    return render_template('uvod.jinja')