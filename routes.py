"""AUCR chat plugin route page handler."""
# coding=utf-8
from aucr_app import db
from flask import Blueprint
from flask import session, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from aucr_app.plugins.Sermo.forms import ChatForm
from aucr_app.plugins.Sermo.models import Rooms, Chat
from aucr_app.plugins.auth.models import User


chat_page = Blueprint('chat', __name__, template_folder='templates')


@chat_page.route('/room/<room>')
@login_required
def chat_room(room):
    """Chat room. The user's name and room must be stored in the session."""
    room = room
    if room == '':
        return redirect(url_for('main.index'))
    return render_template('chat.html', name=current_user.username, room_name=room)


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
            url_for_string = url_for('chat.chat_room', room_name=room)
            return redirect(url_for_string)
        form = ChatForm()
        return render_template('rooms.html', form=form)
    if request.method == 'GET':
        room_list = Rooms.query.all()
        room_dict = {}
        for item in room_list:
            author_name = User.query.filter_by(id=item.author_id).first()
            message_count = len(Chat.query.filter_by(room_name=item.room_name).all())
            item_dict = {"name": item.room_name, "created": item.timestamp, "author": author_name.username,
                         "message_count": message_count}
            room_dict[str(item.id)] = item_dict
        form = ChatForm()
        return render_template('rooms.html', form=form, room_dict=room_dict)
