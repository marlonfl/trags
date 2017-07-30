import sqlite3
import os
import sys
from colorama import init
from colorama import Fore, Style

db_path = "../database/"

def format_tags(tags, val):
    delimiter = " = " + str(val) + ", "
    return delimiter.join(tags) + delimiter[:-2]

def tags_viable(usertags, tags):
    if len(usertags) == 0:
        return False
    for usertag in usertags:
        if usertag not in tags:
            return False
    return True

if __name__ == "__main__":
    if len(sys.argv) > 2 :
        sys.exit(Fore.RED + "Too many parameters given")
    if len(sys.argv) < 2 :
        sys.exit(Fore.RED + "Please specify database name")

    db_name = sys.argv[1]

    if not os.path.exists(db_path + db_name + ".db"):
        sys.exit(Fore.RED + "Database %s doesn't exist" % db_name)

    init()
    connection = sqlite3.connect(db_path + db_name + ".db")
    c = connection.cursor()
    tags = [col[1] for col in c.execute("PRAGMA table_info(Songs)")][2:]
    first = True
    while True:
        if first:
            first = False
        else:
            print("")

        query = input(Style.RESET_ALL + Style.BRIGHT + ">>> Enter search query (Enter :exit to quit): ")
        if query == ":exit":
            break

        songs = {index:name for index, name in enumerate(c.execute("SELECT fulltitle FROM Songs WHERE fulltitle LIKE '%%" + query + "%%'"))}
        if songs == {}:
            print(Fore.RED + "No matches found for query '" + str(query) + "'.")
            continue
        else:
            for index in songs:
                print(Style.RESET_ALL + "    " + str(index) + ": " + str(songs[index][0]))

            inp = input(Style.BRIGHT + "> Pick Track (Enter :query for new query): ")
            if inp == ":query":
                continue
            if inp == ":exit":
                break

            if int(inp) not in songs.keys():
                print(Fore.RED + "    Error: Index not in scope")
                continue

            song_title = str(songs[int(inp)][0])
            print(Style.RESET_ALL + "    Track:  " + song_title)
            row = c.execute("SELECT * FROM Songs WHERE fulltitle = '" + song_title + "'").fetchone()[2:]
            song_tags = [tags[i] for i, tag_val in enumerate(row) if int(tag_val) == 1]
            print(Style.RESET_ALL + "    Tags: " + " ".join(song_tags))
            tags_to_1 = input(Style.BRIGHT + "> Specify new tags: ").split(" ")
            tags_to_0 = input(Style.BRIGHT + "> Specify tags to remove: ").split(" ")
            if tags_viable(tags_to_1, tags):
                c.execute("UPDATE Songs SET " + format_tags(tags_to_1, 1) + " WHERE fulltitle = '" + song_title + "'")
            if tags_viable(tags_to_0, tags):
                c.execute("UPDATE Songs SET " + format_tags(tags_to_0, 0) + " WHERE fulltitle = '" + song_title + "'")
            connection.commit()
            print(Fore.GREEN + "    Successfully updated tags")
