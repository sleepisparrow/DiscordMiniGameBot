import sqlite3


class Database:
    """
    Singleton pattern
    load Data/main.db
    """
    _instance = None

    @staticmethod
    def get_instance():
        if Database._instance is None:
            Database()
        return Database._instance

    def __init__(self):
        if Database._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.connection = sqlite3.connect('Data/main.db')
            Database._instance = self
