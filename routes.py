"""AUCR chat plugin route page handler."""
# coding=utf-8
from flask import Blueprint
from flask import session, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from app.plugins.Sermo.forms import ChatForm
from app.plugins.Sermo import events
from app.plugins.auth.utils import get_group_permission_navbar

chat_page = Blueprint('chat', __name__, template_folder='templates')


@chat_page.route('/', methods=['GET', 'POST'])
@login_required
def chat_index():
    """Login form to enter a room."""
    form = ChatForm()
    if form.validate_on_submit():
        session['room'] = form.room.data
        return redirect(url_for('chat.chat_room'))
    elif request.method == 'GET':
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form, current_user_navbar=get_group_permission_navbar())


@chat_page.route('/room')
@login_required
def chat_room():
    """Chat room. The user's name and room must be stored in the session."""
    room = session.get('room', '')
    if room == '':
        return redirect(url_for('main.index'))
    return render_template('chat.html', name=current_user.username, room=room,
                           current_user_navbar=get_group_permission_navbar())
