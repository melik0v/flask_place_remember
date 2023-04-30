from flask_wtf import FlaskForm, csrf
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddMemoryForm(FlaskForm):
    name = StringField("Title: ", validators=[DataRequired()], render_kw={'placeholder': 'Название'})
    place = StringField("Place", validators=[DataRequired()], render_kw={'id': 'id_place', 'type': 'hidden'})
    description = TextAreaField("Description", render_kw={'placeholder': 'Описание', 'style': 'min-height: 10rem;'})
    submit = SubmitField("Submit", render_kw={'class': 'btn btn-outline-success', 'value': 'Сохранить'})


class AddImageForm(FlaskForm):
    pass
