import time
import utilities
import threading
import math
import gc
import shelve
import heapq
import os

class mstThread (threading.Thread):
    def __init__(self, city, CITIES, visited, cmGlobal, mstCities):
        threading.Thread.__init__(self)
        self.city = city
        self.CITIES = CITIES
        self.visited = visited
        self.cm = cmGlobal
        self.mstCities = mstCities
        
    def run(self):

        """ Using kruskal's algorithm to get MST"""
        global mstCities
        #initialize the initial variables
        mstVisited = set(self.visited)
        mstVisited.add(self.city)
        mstDistance = 0
        mstCM = {}
        subGraphs = []
        unVisitedCities = self.CITIES - len(mstVisited)
        
        #initialize distance matrix
        for coord in self.cm.keys():
            if mstVisited.__contains__(eval(coord)[0]) or mstVisited.__contains__(eval(coord)[1]):
                continue
            else:
                mstCM[eval(coord)] = self.cm[coord]
        
        mstCM = sorted(mstCM.items(), key=lambda t: t[1])        
        mstVisited = set()
        #l = len(distances)
        for distance in mstCM:
            #print i,'/',l, len(mstVisited),'/'
            if distance[1] == 0:
                continue
            else:
                t1 = -1
                t2 = -1
                #check if this edge belongs to any of the exiting visited cities
                for i, subGraph in enumerate(subGraphs):
                    if subGraph.__contains__(distance[0][0]):
                        t1 = i
                    if subGraph.__contains__(distance[0][1]):
                        t2 = i
                
                if t1==t2 and t1!=-1:
                    #both the nodes belong to the same tree, potential loop formation, so ignore
                    continue
                elif t1 != t2 and t1 != -1 and t2 != -1:
                    subGraphs[t1].update(subGraphs[t2])
                    subGraphs.remove(subGraphs[t2])
                elif t1 == -1 and t2 != -1:
                    #if first city does not belong to any tree but second one does, then add first city to second's tree
                    subGraphs[t2].add(distance[0][0])
                    mstVisited.update(subGraphs[t2])
                elif t1 != -1 and t2 == -1:
                    #if second city does not belong to any tree but first one does, then add second city to first's tree
                    subGraphs[t1].add(distance[0][1])
                    mstVisited.update(subGraphs[t1])
                else:
                    #if both the cities doesnot belong to any tree, append them in a new tree
                    newSubGraph = set([distance[0][0],distance[0][1]])
                    subGraphs.append(newSubGraph)
                    mstVisited.update(newSubGraph)
                
                mstDistance+=distance[1]
                if len(mstVisited) == unVisitedCities and len(subGraphs)==1:
                    break
        
        mstCM = None
        mstVisited = None
        subGraphs = None
        gc.collect()        
        self.mstCities[self.city] = mstDistance

def getBestTourLength(cm, CITIES = 0):
    """ Accepts inputVar coordinates and returns best tour length """

    #if cities not sent, try calculating cities from the distance matrix
    if CITIES == 0:
        CITIES = int(math.sqrt(len(cm)))
    
    startSelectionCitiesMST = {}
    mstThreads = []
    
    #selecting start city
    for city in range(CITIES):
        t = mstThread(city, CITIES, set(), cm, startSelectionCitiesMST)
        mstThreads.append(t)
        t.start()
          
    for thread in mstThreads:
        thread.join()
      
    startCity = 0
    minFxStartDistance = -1
    for probableStartCity in range(CITIES): 
        minStartDist = -1   
        for city in range(CITIES):
            if probableStartCity == city:
                continue
            if cm[str((city,probableStartCity))] < minStartDist or minStartDist == -1:
                minStartDist = cm[str((city,probableStartCity))]
        if startSelectionCitiesMST[probableStartCity] + minStartDist < minFxStartDistance or minFxStartDistance == -1:
            minFxStartDistance = startSelectionCitiesMST[probableStartCity] + minStartDist
            startCity = probableStartCity
            
    mstThreads = None
    nextCity = startCity
    visited = [startCity]
    gx = 0
    fxheapq = []
    #continue till all cities are not visited
    while len(visited)!=CITIES:
        currentCity = nextCity
        nextCity = -1
        mstThreads = []
        mstCities = {}
        
        #find mst using kruskals algo creating threads
        for city in range(CITIES):
            #continue if current city is same as in the loop or it has been already visited
            if city == currentCity or visited.__contains__(city):
                continue
            
            cityThread = mstThread(city, CITIES, visited, cm, mstCities)
            cityThread.start()
            mstThreads.append(cityThread)
        
        # Wait for all threads to complete
        for t in mstThreads:
            t.join()    
        
        for city in range(CITIES):
            if city == currentCity or visited.__contains__(city):
                continue    
            #calculate distMinHxNextCity
            distMinHxNextCity = -1
            distMinHxStartCity = -1
            for probableNextcity in range(CITIES):
                if probableNextcity == currentCity or probableNextcity == city or visited.__contains__(probableNextcity):
                    continue 
                if cm[str((probableNextcity,city))] < distMinHxNextCity or distMinHxNextCity == -1:
                    distMinHxNextCity = cm[str((probableNextcity,city))]
                #calculate distMinHxStartCity
                if cm[str((probableNextcity,startCity))] < distMinHxStartCity or distMinHxStartCity == -1:
                    distMinHxStartCity = cm[str((probableNextcity,startCity))]

            #if the distance of the city from current city is less then minDistance assigning this city as the next city
            hx = distMinHxNextCity + distMinHxStartCity #mst of the rest of the cities
            #print "hx", hx
            tempVisited = list(visited)
            tempVisited.append(city)
            heapq.heappush(fxheapq, (gx+hx, tempVisited))
                           
        minRoute = heapq.heappop(fxheapq)
        #Find the minimum fx with maximum length i.e. nextCity
        currentFx = minRoute[0]
        minLength = len(minRoute[1])
        tempFxPushList = [minRoute]
        routeWithMinFxMaxLength = minRoute
        while True: 
            tempMinRoute = heapq.heappop(fxheapq)
            tempFxPushList.append(tempMinRoute)
            if abs(tempMinRoute[0] - currentFx) > 1.0:
                break
            if len(tempMinRoute[1]) > minLength:
                routeWithMinFxMaxLength = tempMinRoute
                minLength = len(tempMinRoute[1])
 
        tempFxPushList.remove(routeWithMinFxMaxLength)
        for fx in tempFxPushList:
            heapq.heappush(fxheapq, fx)
        minRoute = routeWithMinFxMaxLength
        #Finding minhx with max length login end
        
        #change visited  
        visited = minRoute[1]
        gx = utilities.tour_length(cm, visited)
    
    #append start city at the end
    visited.append(startCity)
    return utilities.tour_length(cm, visited)
    
if __name__ == "__main__":
    """ If directly run, calculates best tour Length and time take for calculation for 'att48.tsp' """
    #using shelve file to store distance matrix, so as to avoid memory error
    matrix = shelve.open("tempData")
    matrix.clear()
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
    print "Finding best path, this will take some time, kindly be patient.."
    s = time.time()
    print "Tour length "+ repr(getBestTourLength(utilities.cartesian_matrix(matrix,coords)))
    print "Time taken", round(time.time()-s,4),"seconds"
    matrix.close()