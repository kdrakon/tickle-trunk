#!/usr/bin/python

import threading
import os
import shutil
import subprocess
import time

threadLock = threading.Lock()

class semlibPipelineManager:
	
	def startWatcher(self, folderToWatch):
		#begin watching the folder to perform jobs for
		
		while True:
		
			#retrieve files in the directory. for each file, create a thread to process it.
			for inputFile in os.listdir(folderToWatch):
				newJob = semlibJobThread()
				
				#upon creation of the thread, move the file into another directory so that it is not processed again.
				shutil.move(folderToWatch + inputFile, "./working/" + inputFile)	
				newJob.run("./working/" + inputFile)
				
			#sleep, loop to the top, and start again.
			print "sleeping..."
			time.sleep(5)
            

class semlibJobThread(threading.Thread):
	
    def run(self, inputFile):
        #obtain the lock first (will block until the lock is released)
        threadLock.acquire()

        #if the lock is open, perform following job duties.
        #call subprocess for each individual job of the pipeline
        #once all completed with subprocesses eg. subprocess.call(["ls", "-l"])
            
        subprocess.call(["java", "-version"])
        #subprocess.call preprocessing
        #subprocess.call vectorising
        #subprocess.call mahout similarities
        #subprocess.call postprocessing	

        #RELEASE THE LOCK
        threadLock.release()
        
pipe = semlibPipelineManager()

pipe.startWatcher("./input/")

