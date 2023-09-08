from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response
from app import DAO
from Misc.functions import *

from Controllers.AdminManager import AdminManager
from Controllers.GameManager import GameManager
from Controllers.UserManager import UserManager

admin_view = Blueprint('admin_routes', __name__, template_folder='../templates/admin/', url_prefix='/admin')

game_manager = GameManager(DAO)
user_manager = UserManager(DAO)
admin_manager = AdminManager(DAO)


@admin_view.route('/', methods=['GET'])
@admin_manager.admin.login_required
def home():
	admin_manager.admin.set_session(session, g)

	return render_template('admin/home.html', g=g)


@admin_view.route('/signin/', methods=['GET', 'POST'])
@admin_manager.admin.redirect_if_login
def signin():
	if request.method == 'POST':
		_form = request.form
		email = str(_form["email"])
		password = str(_form["password"])

		if len(email)<1 or len(password)<1:
			return render_template('admin/signin.html', error="Email and password are required")

		d = admin_manager.signin(email, password)

		if d and len(d)>0:
			session['admin'] = int(d["id"])

			return redirect("/admin")

		return render_template('admin/signin.html', error="Email or password incorrect")

	return render_template('admin/signin.html')


@admin_view.route('/signout/', methods=['GET'])
@admin_manager.admin.login_required
def signout():
	admin_manager.signout()

	return redirect("/admin/", code=302)


@admin_view.route('/users/view/', methods=['GET'])
@admin_manager.admin.login_required
def users_view():
	admin_manager.admin.set_session(session, g)

	id = int(admin_manager.admin.uid())
	admin = admin_manager.get(id)
	myusers = admin_manager.getUsersList()

	return render_template('users.html', g=g, admin=admin, users=myusers)



@admin_view.route('/games/', methods=['GET'])
@admin_manager.admin.login_required
def games():
	admin_manager.admin.set_session(session, g)

	id = int(admin_manager.admin.uid())
	admin = admin_manager.get(id)
	mygames = game_manager.list(availability=0)

	return render_template('games/views.html', g=g, games=mygames, admin=admin)

@admin_view.route('/games/<int:id>')
@admin_manager.admin.login_required
def view_game(id):
	admin_manager.admin.set_session(session, g)

	if id != None:
		b = game_manager.getGame(id)
		users = user_manager.getUsersByGame(id)

		print('----------------------------')
		print(users)
		
		if b and len(b) <1:
			return render_template('games/game_view.html', error="No game found!")

		return render_template("games/game_view.html", games=b, games_owners=users, g=g)


@admin_view.route('/games/add', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def game_add():
	admin_manager.admin.set_session(session, g)
	
	return render_template('games/add.html', g=g)


@admin_view.route('/games/edit/<int:id>', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def game_edit(id):
	admin_manager.admin.set_session(session, g)

	if id != None:
		b = game_manager.getGame(id)

		if b and len(b) <1:
			return render_template('edit.html', error="No game found!")

		return render_template("games/edit.html", game=b, g=g)
	
	return redirect('/games')

@admin_view.route('/games/delete/<int:id>', methods=['GET'])
@admin_manager.admin.login_required
def game_delete(id):
	id = int(id)

	if id is not None:
		game_manager.delete(id)
	
	return redirect('/admin/games/')


@admin_view.route('/games/search', methods=['GET'])
def search():
	admin_manager.admin.set_session(session, g)

	if "keyword" not in request.args:
		return render_template("games/view.html")

	keyword = request.args["keyword"]

	if len(keyword)<1:
		return redirect('/admin/games')

	id = int(admin_manager.admin.uid())
	admin = admin_manager.get(id)

	d=game_manager.search(keyword)

	if len(d) >0:
		return render_template("games/views.html", search=True, games=d, count=len(d), keyword=escape(keyword), g=g, admin=admin)

	return render_template('games/views.html', error="No games found!", keyword=escape(keyword))

