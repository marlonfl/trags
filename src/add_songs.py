import sqlite3
import sys
import os

db_path = "../database/"

def build_boolean(tags, usertags):
    return [1 if tag in usertags else 0 for tag in tags]

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

    while True:
        song_url = input("> Enter song url (':exit' to quit): ")

        if song_url == ":exit":
            break

        song_name = input("> Enter song name: ")

        print("> Specify song tags separated by space\nTags: " + ", ".join(tags))
        user_tags = input("> : ").split(" ")
        values = [song_url, song_name] + build_boolean(tags, user_tags)
        #insert_string = "insert into Songs values (" + ",".join(values) + ")"
        #print(insert_string)
        c.execute("INSERT into Songs values (" + ",".join(["?"]*(2+len(tags))) + ")", values)
        #c.execute(insert_string)
        connection.commit()

    connection.close()
    print ("Songs successfully saved")
