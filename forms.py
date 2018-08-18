from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    """Accepts a room name."""
    room = StringField('room', validators=[DataRequired()])
    submit = SubmitField('Join')
