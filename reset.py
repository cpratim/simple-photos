from database import DB
import os

os.system('rm users.db')
os.system('touch users.db')

db = DB('users.db', _init=True)

print('Reset Complete')