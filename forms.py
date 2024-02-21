from wtforms import StringField, PasswordField, SubmitField,SelectField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class PrihlaseniForm(FlaskForm):
    jmeno = StringField('Jméno', validators=[DataRequired()])
    heslo = PasswordField('Heslo', validators=[DataRequired()])
    odeslat = SubmitField('Přihlásit se')

class UserSelectForm(FlaskForm):
    selected_user = SelectField('Vyberte uživatele', coerce=int)
    submit = SubmitField('Zobrazit operace')
    
