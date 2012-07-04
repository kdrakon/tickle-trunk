#!/usr/bin/python

import shutil, os
from mutagen.mp3 import EasyMP3 #from http://code.google.com/p/mutagen/
import sys

for a in sys.argv[1:len(sys.argv)]:

    audio = EasyMP3(a)

    ndArtist = "./" + "".join(audio['artist']) + "/"
    
    ndArtist = ndArtist.replace(" / ", " and ")
    
    ndAlbum = ndArtist + "".join(audio['album']) + "/"

    if not os.path.exists(ndArtist):
        os.mkdir(ndArtist)
        print "made dir: " + ndArtist
        
    if not os.path.exists(ndAlbum): 
        os.mkdir(ndAlbum)
        print "made dir: " + ndAlbum

    shutil.copy2(a, ndAlbum)
    print "copied: " + a
