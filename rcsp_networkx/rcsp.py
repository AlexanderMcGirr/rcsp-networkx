import queue
import rcsp_networkx.defaultclasses
import rcsp_networkx.defaultfunctions

def rcsp(g,source, terminal, 
         resourceExtensionFunction = rcsp_networkx.defaultfunctions.defaultREF, labelDominationFunction = rcsp_networkx.defaultfunctions.defaultLabelDominationFunction, 
         sourceResourceDict = {'cost' : 0 , 'time' :0},
         labelQueue = queue.PriorityQueue, labelDefinition = rcsp_networkx.defaultclasses.Label):
        
    label_number = 1
    numberOfIterations = 0
    
    first_label = labelDefinition(resVert = source)
    first_label.resourceDict = sourceResourceDict
    current_label = None
    new_label = None
    
    # The dictionary should have an empty list for each node that needs a labelList
    labelList = {}
    labelList[source] = []
    
    unprocessed_labels = labelQueue()
    unprocessed_labels.put(first_label)
    
    while not unprocessed_labels.empty():
        current_label = unprocessed_labels.get()
        if(not current_label.isDominated):
            resident_vertex = current_label.residentVertex
            
            # Make sure vertex has an associated label list
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
            # Instead of creating another for loop we use list comprehensions
            labelList[resident_vertex][:] = [lbl for lbl in labelList[resident_vertex]
                                            if not (lbl.isDominated and lbl.isProcessed)]
        
        if(not current_label.isDominated):
            current_label.isProcessed = True
            # g.out_edges returns a tuple with (s,t)
            # forwardStar[0] = Source node
            # forwardStar[1] = Sink node
            for edge in g.out_edges([current_label.residentVertex]):
                new_label = resourceExtensionFunction(g,edge, current_label, label_number)
                edgeTerminal = edge[1]
                if new_label.feasibility:
                    unprocessed_labels.put(new_label.newLabel)
                    if new_label.newLabel.residentVertex not in labelList:
                        labelList[new_label.newLabel.residentVertex] = []
                    labelList[edgeTerminal].append(new_label.newLabel)
                    label_number += 1
        
        # Remove this label from its respective labelList because it is dominated
        else:
            labelList[current_label.residentVertex].remove(current_label)
          
        numberOfIterations +=1
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
        print("Path: ",end='')
        for s in reversed(solution):
            print("{}".format(s.residentVertex), end='')
        print()
        print("Accumulated Costs: {}".format(accumulatedResourceVector))