import sqlite3
import os
import sys

db_path = "../database/"

if __name__ == "__main__":
    if len(sys.argv) > 2 :
        sys.exit("Too many parameters given")
    if len(sys.argv) < 2 :
        sys.exit("Please specify database name")

    db_name = sys.argv[1]

    if (os.path.exists(db_path + db_name + ".db")):
        sys.exit("Database already exists")

    with open("../tags") as f:
        tags = [tag.rstrip() for tag in f.readlines()]

    tags_string = " INTEGER, ".join(tags) + " INTEGER"

    db = sqlite3.connect(db_path + db_name + ".db")
    db_string = "CREATE TABLE Songs (fulltitle TEXT, url TEXT, " + tags_string + ")"
    db.execute(db_string)
