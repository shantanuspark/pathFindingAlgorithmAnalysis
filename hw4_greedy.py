import time
import utilities
import math
import random
import shelve
import os

def getBestTourLength(cm, CITIES = 0):
    """ Accepts input coordinates and returns best tour length """
    
    #if cities not sent, try calculating cities from the distance matrix
    if CITIES == 0:
        CITIES = int(math.sqrt(len(cm)))
        
    startCity = random.randint(0, CITIES)
    nextCity = startCity
    visited = [startCity]
    gx = 0
    
    #continue till all cities are not visited
    while len(visited)!=CITIES:
        currentCity = nextCity
        minDist = -1
        nextCity = -1
        for city in range(CITIES):
            #continue if current city is same as in the loop or it has been already visited
            if city == currentCity or visited.__contains__(city):
                continue
            #if the distance of the city from current city is less then minDistance assigning this city as the next city
            if cm[str((city, currentCity))] < minDist or minDist == -1:
                minDist = cm[str((city, currentCity))]
                nextCity = city
        visited.append(nextCity)
        gx+=cm[str((currentCity, nextCity))]
    
    #append start city at the end
    visited.append(startCity)
    return gx+cm[str((nextCity, startCity))]
    
if __name__ == "__main__":
    """ If directly run, canlcalates best tour Length and time take for calculation for 'att48.tsp' """
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
    print "Finding best path, this may take some time, please be patient.."    
    s = time.time()
    print "Tour length", getBestTourLength(utilities.cartesian_matrix(matrix, coords))
    print "Time taken", round(time.time()-s,4),"seconds"
    matrix.close()