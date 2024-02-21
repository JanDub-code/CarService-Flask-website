from flask import render_template,Blueprint
from functions import odhlášení


odhlaseni = Blueprint("odhlaseni", __name__)


@odhlaseni.route('/odhlaseni')
def odhlas():
    return odhlášení.logout_user()