import sqlite3
from crypto import hash_

class DB(object):

	def __init__(self, file, _init=False):

		self.db_file = file
		self.code = lambda length: ''.join([CHARSET[randint(0, len(CHARSET) - 1)] for char in range(length)])
		self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
		self.cursor = self.connection.cursor()
		if _init: self._init()

	def _init(self):
		self.cursor.execute("CREATE TABLE users(email text PRIMARY KEY, password text, pictures text)")
		self.connection.commit()

	def register(self, email, password):
		self.cursor.execute("SELECT * from users WHERE email=?", (email,))
		fetch = self.cursor.fetchone()
		p = hash_(password)
		if fetch is not None: return False
		self.cursor.execute("INSERT INTO users VALUES(?, ?, ?)", (email, p, ""))
		self.connection.commit()
		return True

	def check(self, email, attempt):
		self.cursor.execute("SELECT password from users WHERE email=?", (email,))
		fetch = self.cursor.fetchone()
		if fetch is None: return None
		if hash_(attempt) == fetch[0]: return True
		return False

	def show(self):
		self.cursor.execute('SELECT * from users')
		fetch = self.cursor.fetchone()
		print(fetch)


if __name__ == '__main__':
	a = Authentication('users.db')
	a.register('cpratim@gmail.com', 'nigger')
	a.show()