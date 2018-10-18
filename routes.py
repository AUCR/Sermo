"""AUCR chat plugin route page handler."""
# coding=utf-8
from app import db
from flask import Blueprint
from flask import session, redirect, url_for, render_template, request, flash
from flask_login import current_user, login_required
from app.plugins.Sermo.forms import ChatForm
from app.plugins.Sermo import events
from app.plugins.Sermo.models import Rooms


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
    if request.method == 'POST':
        form = ChatForm(request.form)
        if form.validate_on_submit():
            room = form.room.data
            test_for_room = Rooms.query.filter_by(room_name=room).first()
            if not test_for_room:
                new_room = Rooms(room_name=room, author_id=current_user.id)
                db.session.add(new_room)
                db.session.commit()
            session['room'] = room
            url_for_string = url_for('chat.chat_room', room=room)
            return redirect(url_for_string)
        return render_template('rooms.html', form=form)
    if request.method == 'GET':
        room_list = Rooms.query.all()
        room_dict = {}
        for item in room_list:
            item_dict = {"name": item.room_name}
            room_dict[str(item.id)] = item_dict
        form = ChatForm()
        form.room.data = session.get('room', '')
        return render_template('rooms.html', form=form, room_dict=room_dict)
