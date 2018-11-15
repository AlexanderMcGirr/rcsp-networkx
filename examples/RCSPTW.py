# Testing if the algorithm works based on Boost example:
# https://www.boost.org/doc/libs/1_68_0/libs/graph/example/r_c_shortest_paths_example.cpp

# Resource constrained shortest path problem with Time Windows
if __name__ == '__main__':
    import rcsp_networkx
    import networkx
    import collections
    
    # Resource extension function
    # This should take the graph, edge, label and number as parameters.
    # Returns : A tuple of (bool,Label)
    # This should return feasibility and the new label
    def REF(g,edge, label, labelNum):
        # Take the edge costs and add them    
        newCost = label.resourceDict['cost'] + g[edge[0]][edge[1]]['cost']
        newTime = label.resourceDict['time'] + g[edge[0]][edge[1]]['time']
        
            
        if newTime < g.node[edge[1]]['earliestTime']:
            newTime = g.node[edge[1]]['earliestTime']
        
        # Create new Dictionary for each label
        newResDict = {'cost':newCost,'time':newTime}    
        
        # Now return a tuple with bool if feasible and new label
        # Create named tuple, first argument feasibility, second argument is the new label
        FeasibilityNewLabel = collections.namedtuple('FeasibilityNewLabel', 'feasibility, newLabel')
        feasible = False
        if newTime <= g.node[edge[1]]['latestTime']:
            feasible = True
        newLabel = FeasibilityNewLabel(feasibility=feasible, newLabel=rcsp_networkx.Label(edge[1],edge, label,newResDict, labelNum))
        
        return newLabel
    
    # Label domination function
    # This function takes two labels as parameters
    # Returns: Label (that is dominated) or None
    def labelDom(firstLabel, secondLabel):
        '''
        Parameters: firstLabel -> First label (should be current_label)
                    secondLabel -> Second label should be in resident vertex list
        
        Return : Label that IS DOMINATED or None if no domination    
        '''
        # This function should return the label that IS dominated
        labelOneLessThanEqual = False
        labelTwoLessThanEqual = False
        for first, second in zip(firstLabel.resourceDict.values(), secondLabel.resourceDict.values()):
            if first < second:
                labelOneLessThanEqual = True
            if second < first:
                labelTwoLessThanEqual = True
            
            # If one label does not dominate then we can stop comparisons
            if labelOneLessThanEqual and labelTwoLessThanEqual:
                break
        
        # If both labelOneLessThanEqual and labelTwoLessThanEqual are None then
        # they are equal over all values in resourceVector, then the tie-breaker is to
        # return the first label
        if (labelOneLessThanEqual == False) and (labelTwoLessThanEqual == False):
            return firstLabel
        
        # If they are both true then one does not dominate the other so return None
        if labelOneLessThanEqual and labelTwoLessThanEqual:
            return None
        
        # labelOne is strictly less than labelTwo in at least one element
        # labelTwo is then dominated
        if labelOneLessThanEqual and (labelTwoLessThanEqual == False):
            return secondLabel
        
        # labelTwo is strictly less than labelOne in at least one element
        # labelOne is then dominated
        if (labelOneLessThanEqual == False) and labelTwoLessThanEqual:
            return firstLabel
    
    g = networkx.DiGraph()
    g.add_node("A", earliestTime = 0, latestTime = 0)
    g.add_node("B", earliestTime = 5, latestTime = 20)
    g.add_node("C", earliestTime = 6, latestTime = 10)
    g.add_node("D", earliestTime = 3, latestTime = 12)
    g.add_node("E", earliestTime = 0, latestTime = 100)
    
    g.add_edge("A", "C", cost=1, time=5)
    g.add_edge("B", "B", cost=2, time=5)
    g.add_edge("B", "D", cost=1, time=2)
    g.add_edge("B", "E", cost=2, time=7)
    g.add_edge("C", "B", cost=7, time=3)
    g.add_edge("C", "D", cost=3, time=8)
    g.add_edge("D", "E", cost=1, time=3)
    g.add_edge("E", "A", cost=1, time=5)
    g.add_edge("E", "B", cost=1, time=5)
    
    
    solutions = rcsp_networkx.rcsp(g, "A", "E",REF, labelDom)
    rcsp_networkx.printRCSP(solutions)