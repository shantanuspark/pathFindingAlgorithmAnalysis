import random
from pyevolve import Consts, Initializators
from pyevolve import Crossovers
from pyevolve import G1DList
from pyevolve import GSimpleGA

random.seed(1024)

def testPredictor(chromosome, test):
    '''
    Predicts the class of test based on the chromosome
    '''
    chromosome = ''.join(map(str, chromosome))
    conditionsOfChromosome = []
    node = 0
    signIdentifier = lambda chromosome,node : 1 if chromosome[0+node*6]=='1' else -1
    #Creates the conditions based on chromosome
    while node<7:
        conditionsOfChromosome.append({"sign":signIdentifier(chromosome, node),"attribute":"x"+repr(int(chromosome[1+node*6:3+node*6], 2)+1), "value":int(chromosome[3+node*6:6+node*6],2)})
        node+=1
    
    #Creates  two-category decision tree classifier based on the chromosome conditions and predicts the class of test 
    if test[conditionsOfChromosome[3]["attribute"]] < conditionsOfChromosome[3]["sign"]*conditionsOfChromosome[3]["value"]:
        if test[conditionsOfChromosome[1]["attribute"]] < conditionsOfChromosome[1]["sign"]*conditionsOfChromosome[1]["value"]:
            if test[conditionsOfChromosome[0]["attribute"]] < conditionsOfChromosome[0]["sign"]*conditionsOfChromosome[0]["value"]:
                test["predicted"] = "w1"
            else:
                test["predicted"] = "w2"
        else:
            if test[conditionsOfChromosome[0]["attribute"]] < conditionsOfChromosome[0]["sign"]*conditionsOfChromosome[0]["value"]:
                test["predicted"] = "w1"
            else:
                test["predicted"] = "w2"
    else:
        if test[conditionsOfChromosome[5]["attribute"]] < conditionsOfChromosome[5]["sign"]*conditionsOfChromosome[5]["value"]:
            if test[conditionsOfChromosome[4]["attribute"]] < conditionsOfChromosome[4]["sign"]*conditionsOfChromosome[4]["value"]:
                test["predicted"] = "w1"
            else:
                test["predicted"] = "w2"
        else:
            if test[conditionsOfChromosome[3]["attribute"]] < conditionsOfChromosome[3]["sign"]*conditionsOfChromosome[3]["value"]:
                test["predicted"] = "w1"
            else:
                test["predicted"] = "w2" 
    
    return test

def evaluator(chromosome):
    """
    Fitness function to evaluate the fittness level of each chromosome
    """
    knownValues = [{"x1":1,"x2":5,"x3":-1, "x4":3, "actual":"w1"}, 
                  {"x1":-1,"x2":5,"x3":2, "x4":2, "actual":"w1"},
                  {"x1":2,"x2":3,"x3":-1, "x4":0, "actual":"w1"},
                  {"x1":-3,"x2":4,"x3":-2, "x4":-1, "actual":"w1"},
                  {"x1":-1,"x2":-3,"x3":1, "x4":2, "actual":"w2"},
                  {"x1":-2,"x2":4,"x3":-3, "x4":0, "actual":"w2"},
                  {"x1":-3,"x2":5,"x3":1, "x4":1, "actual":"w2"},
                  {"x1":1,"x2":2,"x3":0, "x4":0, "actual":"w2"
                   }]
    
    correctlyPredicted = 0
    for value in knownValues:
        if value["actual"] == testPredictor(chromosome.getInternalList(), value)["predicted"]:
            correctlyPredicted+=1
    
    accuracy = float(correctlyPredicted)/len(knownValues)
            
    return accuracy
    
def getBestDecisionTree():
    """ Returns length of the best tour"""    
    
    #7 nodes 6 bits each[1 for sign, 2 for attribute and 3 for value] so 42
    genome = G1DList.G1DList(42)

    genome.evaluator.set(lambda chromosome: evaluator(chromosome))
    genome.crossover.set(Crossovers.G1DListCrossoverSinglePoint)
    genome.initializator.set(Initializators.G1DBinaryStringInitializator)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(100)
    ga.setMinimax(Consts.minimaxType["maximize"])
    ga.setCrossoverRate(0.6)
    ga.setMutationRate(0.01)
    ga.setPopulationSize(15)

    ga.evolve(freq_stats=50)
    
    best = ga.bestIndividual()
    
    return best   
        

if __name__ == "__main__":
    bestChromosome = getBestDecisionTree()
    test1 = {"x1":-1,"x2":4,"x3":1, "x4":1} 
    test2 = {"x1":-2,"x2":4,"x3":-1, "x4":1}
    test3 = {"x1":3,"x2":3,"x3":0, "x4":1}
    print "Predicted class for",test1,"is",testPredictor(bestChromosome.getInternalList(), test1)['predicted']
    print "Predicted class for",test2,"is",testPredictor(bestChromosome.getInternalList(), test2)['predicted']
    print "Predicted class for",test3,"is",testPredictor(bestChromosome.getInternalList(), test3)['predicted']