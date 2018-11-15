#===============================================================================
# Default functions
# Assumptions: 1) cost is the attribute of the cost
#              2) time is an attribute
#              3) The default Label class is used
import collections
import rcsp_networkx.defaultclasses
 
def defaultREF(g,edge, label, labelNum):
        #Unpacking the tuple is faster than indexing it
        (edgeSource, edgeTerminal) = edge        
        newCost = label.resourceDict['cost'] + g[edgeSource][edgeTerminal]['cost']
        newTime = label.resourceDict['time'] + g[edgeSource][edgeTerminal]['time']
        
        newResDict = { 'cost' : newCost, 'time' : newTime }
        feasible = True
        
        FeasibilityNewLabel = collections.namedtuple('FeasibilityNewLabel', 'feasibility, newLabel')
        newLabel = FeasibilityNewLabel(feasibility=feasible, newLabel=rcsp_networkx.defaultclasses.Label(edgeTerminal,edge, label,newResDict, labelNum))
                
        return newLabel
  
def defaultLabelDominationFunction(firstLabel, secondLabel):
        if firstLabel.resourceDict['cost'] <= secondLabel.resourceDict['cost']:
            return secondLabel
        elif secondLabel.resourceDict['cost'] <= firstLabel.resourceDict['cost']:
            return firstLabel
        else:
            return None
#===============================================================================