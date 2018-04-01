"""AUCR chat plugin."""
# coding=utf-8
from app.plugins.Sermo.routes import chat_page
from app.plugins.Sermo import routes, events


def load(app):
    """AUCR chat plugin flask app blueprint registration."""
    app.register_blueprint(chat_page, url_prefix='/chat')
