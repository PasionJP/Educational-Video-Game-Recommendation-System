from App.Games import Games

class GameManager():
	def __init__(self, DAO):
		self.misc = Games(DAO.db.game)
		self.dao = self.misc.dao

	def list(self, availability=1,user_id=None):
		if user_id!= None:
			game_list = self.dao.listByUser(user_id)
		else:
			game_list = self.dao.list(availability)

		return game_list

	def getReserverdGamesByUser(self, user_id):
		games = self.dao.getReserverdGamesByUser(user_id)

		return games

	def getGame(self, id):
		games = self.dao.getGame(id)

		return games

	def search(self, keyword):
		games = self.dao.search_game(keyword)

		return games

	def reserve(self, user_id, game_id):
		games = self.dao.reserve(user_id, game_id)

		return games

	def getUserGames(self, user_id):
		games = self.dao.getGamessByUser(user_id)

		return games

	def getUserGamesCount(self, user_id):
		games = self.dao.getGamesCountByUser(user_id)

		return games

	def delete(self, id):
		self.dao.delete(id)