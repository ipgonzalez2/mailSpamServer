from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length
class FilterForm(FlaskForm):
    porcentaje = SelectField('Caracteres comprobados', choices=[('4', '4%'), ('5', '5%'), ('6', '6%'), ('7', '7%')])
    submit = SubmitField('Guardar')