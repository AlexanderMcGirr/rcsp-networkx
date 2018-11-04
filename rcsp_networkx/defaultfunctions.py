#===============================================================================
# Default functions
# Assumptions: 1) cost is the attribute of the cost
#              2) time is an attribute
#              3) The default Label class is used
import rcsp_networkx.defaultclasses
 
def defaultREF(g,edge, label, labelNum):
        newCost = label.resourceDict['cost'] + g[edge[0]][edge[1]]['cost']
        newTime = label.resourceDict['time'] + g[edge[0]][edge[1]]['time']
          
        newResDict = { 'cost' : newCost, 'time' : newTime }
        feasible = True
          
        return (feasible, rcsp_networkx.defaultclasses.Label(edge[1], edge, label, newResDict, labelNum))
  
def defaultLabelDominationFunction(firstLabel, secondLabel):
        if firstLabel.resourceDict['cost'] <= secondLabel.resourceDict['cost']:
            return secondLabel
        elif secondLabel.resourceDict['cost'] <= firstLabel.resourceDict['cost']:
            return firstLabel
        else:
            return None
#===============================================================================