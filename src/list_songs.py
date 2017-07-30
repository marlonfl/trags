import sqlite3
import sys
import os
# cur.execute("UPDATE Songs Set hype = 1 WHERE url = 'https://www.youtube.com/watch?v=raE6z8IrNn0'")
# HOPE U THINKING BOUT ME fehlen tags, sampled soundcloud trap beat lofi internet chill

db_path = "../database/"

if __name__ == "__main__":
    if len(sys.argv) > 2 :
        sys.exit("Too many parameters given")
    if len(sys.argv) < 2 :
        sys.exit("Please specify database name")

    db_name = sys.argv[1]

    if not os.path.exists(db_path + db_name + ".db"):
        sys.exit("Database %s doesn't exist" % db_name)

    connection = sqlite3.connect(db_path + db_name + ".db")
    c = connection.cursor()
    tags = [col[1] for col in c.execute("PRAGMA table_info(Songs)")][2:]

    c.execute("select * from Songs")
    for s in c.execute("select * from Songs"):
        url = s[0]
        print(s)
