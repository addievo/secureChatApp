#intiialise database
def init_db():
    return sqlite3.connect(DATABASE)