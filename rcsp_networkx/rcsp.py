import queue

class Label():
    ''' 
    According to Boost documentation labels in SPPRC stores:
        
        -Resident vertex
        -Predecessor Arc over which it has been extended
        -Predecessor label
        -Current Vector of resource values    
    '''
    def __init__(self, resVert=None,predEdge=None,predLabel=None,resDict = {},labelID=0):
        '''
        TODO: Need a way for label to have the resourceVectors converted to resourceDictionaries
        
        '''
        self.residentVertex = resVert
        self.predEdge = predEdge
        self.predLabel = predLabel
        self.resourceDict = resDict
        self.isDominated = False
        self.isProcessed = False
        self.isFeasible = True
        self.id = labelID
    
    def __eq__(self,other):
        return (self.id == other.id)
    
    def __ne__(self,other):
        return (self.id != other.id)
    
    def __lt__(self,other):
        return (self.id < other.id)
    
    def __le__(self,other):
        return (self.id <= other.id)
    
    def __gt__(self,other):
        return (self.id > other.id)
    
    def __ge__(self,other):
        return (self.id >= other.id)



def rcsp(g,source, terminal, resourceExtensionFunction, labelDominationFunction):
    
    label_number = 1
    numberOfIterations = 0
    
    first_label = Label(resVert = source)
    first_label.resourceDict = {'cost' : 0 , 'time' : 0}
    current_label = None
    new_label = None
    
    # The dictionary should have an empty list for each node that needs a labelList
    labelList = {}
    labelList[source] = []
    
    unprocessed_labels = queue.PriorityQueue()
    unprocessed_labels.put(first_label)
    
    while not unprocessed_labels.empty():
        current_label = unprocessed_labels.get()
        if(not current_label.isDominated):
            resident_vertex = current_label.residentVertex
            
            if resident_vertex not in labelList:
                labelList[resident_vertex] = []
            
            for vertexLabel in labelList[resident_vertex]:
                # labelDom will return the label that IS DOMINATED.
                # This function is also defined in the Graph class
                labelDom = None
                if current_label != vertexLabel:
                    labelDom = labelDominationFunction(current_label, vertexLabel)
                if (labelDom is not None):
                    labelDom.isDominated = True
            
            # See https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating
            # Cannot remove an item from list while iterating over it in the above for loop
            labelList[resident_vertex][:] = [lbl for lbl in labelList[resident_vertex] 
                                            if not (lbl.isDominated and lbl.isProcessed)]
        
        if(not current_label.isDominated):
            current_label.isProcessed = True
            # g.out_edges returns a tuple with (s,t)
            # forwardStar[0] = Source node
            # forwardStar[1] = Sink node
            for forwardStar in g.out_edges([current_label.residentVertex]):
                new_label = resourceExtensionFunction(g,forwardStar, current_label, label_number)
                if new_label[0]:
                    unprocessed_labels.put(new_label[1])
                    if new_label[1].residentVertex not in labelList:
                        labelList[new_label[1].residentVertex] = []
                    labelList[forwardStar[1]].append(new_label[1])
                    label_number += 1
            
        
        # Remove this label from its respective labelList because it is dominated
        else:
            labelList[current_label.residentVertex].remove(current_label)
        
        numberOfIterations +=1
     
    print("Number of Iterations: {}".format(numberOfIterations))
    
    # Returns a list of labels that are feasible    
    return labelList[terminal]

def printRCSP(labelList):
    paretoSolutions = []
    for solution in labelList:
        # Create a new list for each solution
        tempList = []
        labelIterator = solution
        # Take the first terminal label and append to list
        while labelIterator:
            tempList.append(labelIterator)
            labelIterator = labelIterator.predLabel
        paretoSolutions.append(tempList)
    
    # For each solution print in reverse order
    for solution in paretoSolutions:
        accumulatedResourceVector = solution[0].resourceDict
        print("Path:",end='')
        for s in reversed(solution):
            print("{}".format(s.residentVertex), end='')
        print()
        print("Accumulated Costs: {}".format(accumulatedResourceVector))