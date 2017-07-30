import sqlite3
import os
import sys
import youtube_dl
import vlc
import time
from random import shuffle
from colorama import init
from colorama import Fore, Style

db_path = "../database/"

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def format_tags(tags, val):
    delimiter = " = " + str(val) + " AND "
    return delimiter.join(tags) + delimiter[:-5]

def tags_viable(usertags, tags):
    if len(usertags) == 0:
        return False
    for usertag in usertags:
        if usertag not in tags:
            return False
    return True

if __name__ == "__main__":
    init()
    if len(sys.argv) > 2 :
        sys.exit(Fore.RED + "Too many parameters given")
    if len(sys.argv) < 2 :
        sys.exit(Fore.RED + "Please specify database name")

    db_name = sys.argv[1]

    if not os.path.exists(db_path + db_name + ".db"):
        sys.exit(Fore.RED + "Database %s doesn't exist" % db_name)

    connection = sqlite3.connect(db_path + db_name + ".db")
    c = connection.cursor()
    tags = [col[1] for col in c.execute("PRAGMA table_info(Songs)")][2:]

    print("Tags: " + " ".join(tags))
    usertags = input("Enter Tags: ")
    groups = [split.split(" ") for split in usertags.split(" or ")]

    for group in groups:
        if not tags_viable(group, tags):
            sys.exit(Fore.RED + "Invalid Tag found")

    songs = []
    for group in groups:
        for song in c.execute("SELECT * FROM Songs WHERE " + format_tags(group, 1)):
            songs.append(song[0:2])

    shuffle(songs)
    unique_songs = set(songs)

    for song in unique_songs:
        print("Downloading " + song[1] + "...")
        os.system("youtube-dl -x --audio-format mp3 --audio-quality 192K --id -q " + song[0])
        vid_id = song[0].split("?v=")[1]
        print("    Finished downloading " + song[1])
        os.system("mv " + vid_id + ".mp3 ../temp/" + vid_id + ".mp3")
        print(Fore.GREEN + "Playing " + song[1] + Style.RESET_ALL)
        p = vlc.MediaPlayer("/home/marlon/code/trags/trags/temp/" + vid_id + ".mp3")
        print(p.audio_get_volume())
        p.audio_set_volume(95)
        p.play()

        while (p.get_position() > -1 and p.get_position() < 0.98):
            pass
