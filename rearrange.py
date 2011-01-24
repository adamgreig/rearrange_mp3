# Reorganise an MP3 collection, copying all .mp3 files found in one folder to a
# new file structure in another folder based on ID3 tag data.
#
# Copyright 2011 Adam Greig. Released into the public domain.

import sys
import os
import shutil
import string
import re
from mutagen.easyid3 import EasyID3

regex = re.compile("\W")

if len(sys.argv) != 3:
    print "Usage:"
    print sys.argv[0], "<source directory>", "<target directory>"
    print
    sys.exit(0)

if not os.path.isdir(sys.argv[1]) or not os.path.isdir(sys.argv[2]):
    print "invalid source or target specified: not a directory"
    sys.exit(0)

source = sys.argv[1]
target = sys.argv[2]

print "Copying files from", source

for root, dirs, files in os.walk(source):
    print "  Now in", root
    for f in files:
        ext = f.split(".")[-1]
        if ext.lower() == "mp3":
            song = root + os.sep + f
            try:
                print "    Processing", song
                tag = EasyID3(song)
                num = tag["tracknumber"][0]
                title = tag["title"][0]
                album = tag["album"][0]
                artist = tag["artist"][0]
            except (KeyError, IndexError):
                print "    * Error getting ID3 info, skipping."
                continue
            else:
                num = regex.sub("_", num)
                title = regex.sub("_", title)
                album = regex.sub("_", album)
                artist = regex.sub("_", artist)
                print num, title, album, artist
