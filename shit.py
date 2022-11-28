import sqlite3


database = sqlite3.connect("db.db")

cur = database.cursor()

cur.execute("DROP TABLE IF EXISTS sounds")
cur.execute("CREATE TABLE IF NOT EXISTS sounds (name, path)")

# cur.execute("INSERT INTO sounds VALUES (?, ?)", ("mac", "test.flac"))
# cur.execute("INSERT INTO sounds VALUES (?, ?)", ("fbi", "test.mp3"))

# cur.execute("DROP TABLE shortcuts")
cur.execute("CREATE TABLE IF NOT EXISTS shortcuts (key, sound)")

# cur.execute("INSERT INTO shortcuts VALUES ('1', '1')")
# cur.execute("INSERT INTO shortcuts VALUES ('2', '2')")

database.commit()