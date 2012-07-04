#!/usr/bin/python

import sys
import subprocess
import time
import os
import shutil

input_directory = "input"
output_directory = "output"
watermarkfile = "watermark/watermark.gif"


def processImages(dir):
    
    items = os.listdir(dir)
    
    for item in items:
        
        itemLocation = dir + "/" + item
        
        if os.path.isfile(itemLocation):
            inputimagefile = itemLocation
            outputimagefile = output_directory + "/" + itemLocation            
            try:
                os.makedirs(output_directory + "/" + dir)
            except:
                print "Directory exists..."
            
            # composite -dissolve 30% -gravity southeast watermark.gif images/sample_01.jpg output.jpg
            p = ["composite", "-dissolve", "30%", "-gravity", "southeast", watermarkfile, inputimagefile, outputimagefile]
            print "processing " + inputimagefile
            subprocess.call(p)
            print "done"
            
        elif os.path.isdir(itemLocation):
            print "Going into " + itemLocation + "..."
            processImages(itemLocation)

def main(args):
    
    processImages(input_directory)    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
