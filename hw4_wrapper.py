import gzip
import hw4_greedy
import time
import pyevolve_ex12_tsp
import utilities
import threading
import os.path
import shelve

class fileEvaluatorThread(threading.Thread):
    def __init__(self, gzipFile):
        threading.Thread.__init__(self)
        self.gzipFile = gzipFile
    
    def run(self):
        with gzip.open('./data/'+self.gzipFile, 'rb') as inputFile:
            coords = utilities.getCoords(inputFile)
            if coords == -1 or len(coords) == 0:
                return 0
            
            CITIES = len(coords)
            fileName = inputFile.name
            
            cm = ""
            if os.path.isfile(inputFile.name.split("/")[2]+"_cm_shelf"):
                print "Using previously saved distance matrix of this file, if the data in the file was modified kindly delete the _shelf file correspoinding to this file\n"
                cm = shelve.open(inputFile.name.split("/")[2]+"_cm_shelf")
            else:
                print "Distance matrix not found, calculating new one.. "+fileName+"\n"
                cm = shelve.open(inputFile.name.split("/")[2]+"_cm_shelf")
                cm = utilities.cartesian_matrix(cm, coords)
                print "Distances calculation done for "+fileName+"\n"
            
            
            fileName = inputFile.name.split("/")[2]
            try:
                fw = open(fileName+"_greedy_output_"+repr(time.time())+".txt",'w')
                print "Applying Greedy Algorithm on "+inputFile.name+"\n"
                ##Compute tour length and time using greedy
                start = time.time()
                length = hw4_greedy.getBestTourLength(cm, CITIES=CITIES)
                end = time.time()
                fw.write("{'inputFileName':'"+inputFile.name+"', 'algorithm':'greedy', 'bestPathLength':"+repr(length)+"', 'timeTaken':'"+repr(end-start)+"'}\n")
                print "Greedy algorithm finished on "+inputFile.name+". Result saved in "+fw.name+"\n"
                fw.close()
                 
                fw = open(fileName+"_genetic_output_"+repr(time.time())+".txt",'w')
                print "Applying Genetic Algorithm on "+inputFile.name+"\n"
                ##Compute tour length and time using genetic
                start = time.time()
                length = pyevolve_ex12_tsp.getBestTourLength(cm, CITIES=CITIES)
                end = time.time()
                fw.write("{'inputFileName':'"+inputFile.name+"', 'algorithm':'genetic', 'bestPathLength':"+repr(length)+"', 'timeTaken':'"+repr(end-start)+"'}\n")
                print "Genetic algorithm finished on "+inputFile.name+". Result saved in "+fw.name+"\n"
                fw.close()
            except:
                print "Issue with the old shelf file, kindly delete and run again.."    
            finally:
                cm.close()

gzippedFiles = next(os.walk('./data/'))[2]

totalFiles = len(gzippedFiles)
currentFile = 0
threads = []

# Wait for all threads to complete
def wait():
    for t in threads:
        t.join() 

for gzipFile in gzippedFiles:
    if not gzipFile.__contains__('.gz'):
        continue
    try:
        t = fileEvaluatorThread(gzipFile)
        t.start()
        threads.append(t)
        #Running only one thread to avoid memory error
        if len(threads)==1:
            wait()
    except IOError:
        continue


        