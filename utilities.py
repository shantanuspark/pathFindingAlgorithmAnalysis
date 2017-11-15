from math import sqrt
import re
import threading

def readInputFile(filename):
    """ Reads input file """
    coords = []
    try:
        with open(filename, 'r') as inputFile:
            coords = getCoords(inputFile)
    except IOError:
        print("Input file not found, exiting..")
    except EOFError:
        print "EOF reached" 
    return coords

def getCoords(inputFile):
    """ Returns coordinates from input file """
    coords = []
    for line in inputFile:
        try:
            line = re.sub(' +',' ',line.strip())
            words = line.split(" ")
            if words[0]=='EDGE_WEIGHT_TYPE' and not (words[2] == 'EUC_2D' or words[2] == 'ATT'):
                return -1
            float(words[0])
            coords.append((float(words[1]), float(words[2])))
        except:
            continue
    return coords

class cm_thread(threading.Thread):
    def __init__(self, coords, matrix, i, x1, y1):
        threading.Thread.__init__(self)
        self.matrix = matrix
        self.i=i
        self.x1=x1
        self.y1=y1
        self.coords=coords
    def run(self):
        for j, (x2, y2) in enumerate(self.coords):
            dx, dy = self.x1 - x2, self.y1 - y2
            dist = sqrt(dx * dx + dy * dy)
            self.matrix[str((self.i, j))] = dist
            
def cartesian_matrix(matrix, coords):
    """ creates distance matrix """
    
    threads = []
    
    for i, (x1, y1) in enumerate(coords):
        t = cm_thread(coords, matrix, i, x1, y1)
        t.start()
        #Executing only one thread since shelf is not thread safe
        t.join()
        threads.append(t)
        
    return matrix

def tour_length(matrix, tour, isGA=False):
    """ Returns the total length of the tour """
    total = 0
    CITIES = len(tour)
    
    if isGA:
        tour = tour.getInternalList()
        
    for i in range(CITIES):
        j = (i + 1) % CITIES
        total += matrix[str((tour[i], tour[j]))]
    return total
