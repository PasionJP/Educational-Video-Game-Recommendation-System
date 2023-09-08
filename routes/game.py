from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response
from app import DAO

from Controllers.UserManager import UserManager
from Controllers.GameManager import GameManager
import mysql.connector

game_view = Blueprint('game_routes', __name__, template_folder='/templates')

game_manager = GameManager(DAO)
user_manager = UserManager(DAO)
b = {}

@game_view.route('/games/', defaults={'id': None})
@game_view.route('/games/<int:id>')
def home(id):
	user_manager.user.set_session(session, g)

	if id != None:
		b = game_manager.getGame(id)

		print('----------------------------')
		print(b)

		user_games={}
		if user_manager.user.isLoggedIn():
			user_games = game_manager.getReserverdGamesByUser(user_id=user_manager.user.uid())['user_games'].split(',')
		
		if b and len(b) <1:
			return render_template('game_view.html', error="No game found!")

		return render_template("game_view.html", games=b, g=g, user_games=user_games)
	else:
		b = game_manager.list()

		user_games=[]
		if user_manager.user.isLoggedIn():
			reserved_games = game_manager.getReserverdGamesByUser(user_id=user_manager.user.uid())
			
			if reserved_games is not None:
				user_games = reserved_games['user_games'].split(',')
		
		print("---------------------------------------")
		# print("USER GAME", user_games)
		# print("Games", b)
		if b and len(b) <1:
			return render_template('games.html', error="No games found!")
		return render_template("games.html", games=b, g=g, user_games=user_games)


	return render_template("games.html", games=b, g=g)

def checkIfGameDupli(user_id, game_id):
	mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="",
	database="gamesdb"
	)

	mycursor = mydb.cursor()
	mycursor.execute("SELECT 1 FROM reserve WHERE user_id = '{}' AND game_id = '{}';".format(user_id, game_id))
	myresult = mycursor.fetchall()
	# print("EXIST?", myresult)
	if myresult:
		return True
	else:
		return False


@game_view.route('/games/add/<id>', methods=['GET'])
@user_manager.user.login_required
def add(id):
	global b
	user_id = user_manager.user.uid()
	exists = checkIfGameDupli(user_id, id)
	if exists:
		b = game_manager.list()
		user_manager.user.set_session(session, g)
		
		return render_template("games.html", msg="Game already added", games=b, g=g)
	else:
		game_manager.reserve(user_id, id)

		b = game_manager.list()
		user_manager.user.set_session(session, g)
		
		return render_template("games.html", msg="Game added", games=b, g=g)


@game_view.route('/games/search', methods=['GET'])
def search():
	user_manager.user.set_session(session, g)

	if "keyword" not in request.args:
		return render_template("search.html")

	keyword = request.args["keyword"]

	if len(keyword)<1:
		return redirect('/games')

	d=game_manager.search(keyword)

	if len(d) >0:
		for game in d:
			gameId = game['appid']
			# # URL of the Steam game page
			# steam_game_url = 'https://store.steampowered.com/app/' + str(gameId)

			# # Send a GET request to the URL
			# response = requests.get(steam_game_url)

			# # Parse the HTML content with Beautiful Soup
			# soup = BeautifulSoup(response.content, 'html.parser')

			# # Find the image element with the class "game_header_image_full"
			# image_element = soup.find("img", class_="game_header_image_full")

			# # Get the 'src' attribute from the image element
			# if image_element:
			# 	image_source = image_element['src']
			# 	print("Image Source:", image_source)
			# else:
			# 	print("Image source not found.")
		return render_template("games.html", search=True, games=d, count=len(d), keyword=escape(keyword), g=g)

	return render_template('games.html', error="No games found!", keyword=escape(keyword))