from copy import copy

from Models.GameDAO import GameDAO
from Models.UserDAO import UserDAO
from Models.AdminDAO import AdminDAO

from Models.DB import DB

class DBDAO(DB):
	def __init__(self, app):
		super(DBDAO, self).__init__(app)

		self.game = GameDAO(copy(self))
		self.user = UserDAO(copy(self))
		self.admin = AdminDAO(copy(self))
