from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from views import models,auth_blueprint,prihlaseni_blueprint,sprava_uzivatele_blueprint,sprava_vozidel_blueprint,plánování_a_kalendar_blueprint,zpravy_statistiky_blueprint,odhlaseni_blueprint,stav_blueprint
from functions import přihlášení,config,zaregistrování


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaze.db'  # SQLite databáze
app.secret_key = config.secret_key

app.register_blueprint(auth_blueprint.auth_bp, url_prefix='/')
app.register_blueprint(prihlaseni_blueprint.prihlas,url_prefix='/')
app.register_blueprint(sprava_uzivatele_blueprint.sprava_uzivatele,url_prefix='/')
app.register_blueprint(sprava_vozidel_blueprint.sprava_vozidel,url_prefix='/')
app.register_blueprint(plánování_a_kalendar_blueprint.planovani_kalendar,url_prefix='/')
app.register_blueprint(zpravy_statistiky_blueprint.zpravy_statistiky,url_prefix='/')
app.register_blueprint(odhlaseni_blueprint.odhlaseni,url_prefix='/')
app.register_blueprint(stav_blueprint.stav,url_prefix='/')


if __name__ == '__main__':
    with app.app_context():
        models.initialize_db(app)
    app.run()
   