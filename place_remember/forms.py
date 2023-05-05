from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FormField, MultipleFileField
from wtforms.validators import DataRequired, ValidationError


def validate_images(images):
        for file in images.data:
            # File extension check
            extension = file.filename.lower().split('.')[-1]
            if extension not in images.extensions:
                raise ValidationError('Images only!')
            

class AddImageForm(FlaskForm):
    images = MultipleFileField('Select images')

    


class AddMemoryForm(FlaskForm):
    name = StringField('Title: ', validators=[DataRequired()], render_kw={'placeholder': 'Название'})
    place = StringField('Place', validators=[DataRequired()], render_kw={'id': 'id_place', 'type': 'hidden'})
    description = TextAreaField('Description', render_kw={'placeholder': 'Описание', 'style': 'min-height: 10rem;'})
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-outline-success', 'value': 'Сохранить'})
    images = FormField(AddImageForm, 'Images')
