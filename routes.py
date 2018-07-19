"""AUCR chat plugin route page handler."""
# coding=utf-8
from flask import Blueprint
from flask import session, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from app.plugins.Sermo.forms import ChatForm
from app.plugins.Sermo import events


chat_page = Blueprint('chat', __name__, template_folder='templates')


@chat_page.route('/room/<room>')
@login_required
def chat_room(room):
    """Chat room. The user's name and room must be stored in the session."""
    room = room
    if room == '':
        return redirect(url_for('main.index'))
    return render_template('chat.html', name=current_user.username, room=room)


@chat_page.route('/', methods=['GET', 'POST'])
@login_required
def chat_index():
    """Login form to enter a room."""
    form = ChatForm()
    if form.validate_on_submit():
        room = form.room.data
        session['room'] = room
        url_for_string = url_for('chat.chat_room', room=room)
        return redirect(url_for_string)
    elif request.method == 'GET':
        form.room.data = session.get('room', '')
        return render_template('rooms.html', form=form)



