from tinydb import TinyDB

class Database():

    def __init__(self):
        # TODO move in memory
        db = TinyDB('temp_db.json')

    def exists(self):
        pass