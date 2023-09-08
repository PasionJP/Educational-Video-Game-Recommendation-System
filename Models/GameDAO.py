class GameDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "games"

	def delete(self, id):
		q = self.db.query("DELETE FROM @table where id={}".format(id))
		self.db.commit()

		return q

	def reserve(self, user_id, game_id):
		if not self.available(game_id):
			return "err_out"

		q = self.db.query("INSERT INTO reserve (user_id, game_id) VALUES('{}', '{}');".format(user_id, game_id))

		# self.db.query("UPDATE @table set count=count-1 where id={};".format(game_id))
		self.db.commit()

		return q

	def getGamesByUser(self, user_id):
		q = self.db.query("select * from @table left join reserve on reserve.game_id = @table.id where reserve.user_id={}".format(user_id))

		games = q.fetchall()

		return games

	def getGamesCountByUser(self, user_id):
		q = self.db.query("select count(reserve.game_id) as games_count from @table left join reserve on reserve.game_id = @table.id where reserve.user_id={}".format(user_id))

		games = q.fetchall()

		return games

	def getGame(self, id):
		q = self.db.query("select * from @table where id={}".format(id))

		game = q.fetchone()

		print(game)
		return game

	def available(self, id):
		game = self.getById(id)

		return True

	def getById(self, id):
		q = self.db.query("select * from @table where id='{}'".format(id))

		game = q.fetchone()

		return game

	def list(self, availability=1):
		query="select * from @table"
		# Usually when no-admin user query for game
		if availability==1: query= query
		
		games = self.db.query(query)
		
		games = games.fetchall()


		return games

	def getReserverdGamesByUser(self, user_id):
		query="select concat(game_id,',') as user_games from reserve WHERE user_id={}".format(user_id)
		
		games = self.db.query(query)
		
		games = games.fetchone()

		return games

	def search_game(self, name):
		query="select * from @table where name LIKE '%{}%'".format(name)

		# # Usually when no-admin user query for game
		# if availability==1: query= query+"  AND availability={}".format(availability)

		q = self.db.query(query)
		games = q.fetchall()
		
		return games