from flask import Flask, g, escape, session, redirect, render_template, request, jsonify, Response
from Misc.functions import *

app = Flask(__name__)
app.secret_key = '#$ab9&^BB00_.'

# Setting DAO Class
from Models.DAO import DAO

DAO = DAO(app)

from Controllers.UserManager import UserManager
user_manager = UserManager(DAO)


# Registering blueprints
from routes.user import user_view
from routes.game import game_view
from routes.admin import admin_view
from routes.reco import reco_view

# Registering custom functions to be used within templates
app.jinja_env.globals.update(
    ago=ago,
    str=str,
)

app.register_blueprint(user_view)
app.register_blueprint(game_view)
app.register_blueprint(admin_view)
app.register_blueprint(reco_view)

@app.context_processor
def getUsername(id=None):
    if "user" in session and session['user'] != None:
        user_manager.user.set_session(session, g)
        
        if id is None:
            id = int(user_manager.user.uid())
        
        username = user_manager.get(id)
        return {'username': username['name']}
    elif "admin" in session and session['admin'] != None:
        return ""
    else:
        return ""
