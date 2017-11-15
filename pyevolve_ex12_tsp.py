import utilities
import random
import os
import time
from pyevolve import Consts
from pyevolve import Crossovers
from pyevolve import G1DList
from pyevolve import GSimpleGA
import math
import shelve

random.seed(1024)

cmGlobal = []
coords = []
LAST_SCORE = -1

def write_tour_to_file(tour):
    """ The function to write output to file """
    fw = open("output_cities.txt",'w')
    fw.write("TOUR_SECTION\n")
    for city in tour.genomeList:
        fw.write(repr(city+1)+"\n")
    fw.close()
    print "Output is saved in output_cities.txt file at "+os.path.realpath("output_cities.txt")

def G1DListTSPInitializator(genome, **args):
    """ The initializator for the TSP """
    lst = [i for i in xrange(genome.getListSize())]
    random.shuffle(lst)
    genome.setInternalList(lst)

def getBestTourLength(cm, CITIES=0 , writeOutputToFile = False):
    """ Returns length of the best tour"""    
    global cityCount, cmGlobal
    cityCount = CITIES
    cmGlobal = cm
        #if cities not sent, try calculating cities from the distance matrix
    if CITIES == 0:
        cityCount = int(math.sqrt(len(cm)))

    
    genome = G1DList.G1DList(cityCount)

    genome.evaluator.set(lambda chromosome: utilities.tour_length(cm, chromosome, True))
    genome.crossover.set(Crossovers.G1DListCrossoverEdge)
    genome.initializator.set(G1DListTSPInitializator)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(1000)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(1)
    ga.setMutationRate(0.02)
    ga.setPopulationSize(80)

    ga.evolve(0)
    
    best = ga.bestIndividual()
    if writeOutputToFile:
        write_tour_to_file(best)
    
    return utilities.tour_length(cm, best, True)   
        

if __name__ == "__main__":
    #using shelve file to store distance matrix, so as to avoid memory error
    matrix = shelve.open("tempData")
    selectedFile = ""
    while True:
        try:
            inputVar = "Which .tsp you want to use for execution?\n"
            files = next(os.walk('./data/'))[2]
            inputTsps = {}
            i = 0
            for tspFile in files:
                if tspFile.__contains__('.tsp') and not tspFile.__contains__('.tsp.gz'):
                    i+=1
                    inputTsps[i]=tspFile
            if len(tspFile) == 0:
                print "No .tsp file found in /data folder! Please create a data folder in the folder containing the python scripts and place the .tsp file inside it"
                exit()
            for inputTsp in inputTsps.keys():
                inputVar+=str(inputTsp)+". "+inputTsps[inputTsp]+"\n"
            i = int(raw_input(inputVar))
            if int(i)>len(inputTsps) or int(i)<0:
                print "Please enter correct option"
                continue
            selectedFile = inputTsps[i]
            break
        except:
            print "Please enter correct option"
    coords = utilities.readInputFile(filename='./data/'+selectedFile)
    matrix.clear()
    print "Finding best path, this will take some time, kindly be patient.."
    s = time.time()
    print "Tour length "+ repr(getBestTourLength(utilities.cartesian_matrix(matrix, coords), writeOutputToFile = True))
    print "Time taken", round(time.time()-s,4),"seconds"
    matrix.close()