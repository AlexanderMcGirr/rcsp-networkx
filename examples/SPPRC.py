# Testing if the algorithm works based on Boost example:
# https://www.boost.org/doc/libs/1_68_0/libs/graph/example/r_c_shortest_paths_example.cpp

# Traditional Shortest Path Problem
if __name__ == '__main__':
    import rcsp_networkx
    import networkx
    
    def labelDom(firstLabel, secondLabel):
        if firstLabel.resourceDict['cost'] <= secondLabel.resourceDict['cost']:
            return secondLabel
        elif secondLabel.resourceDict['cost'] <= firstLabel.resourceDict['cost']:
            return firstLabel
        else:
            return None
    
    def REF(g,edge, label, labelNum):
        newCost = label.resourceDict['cost'] + g[edge[0]][edge[1]]['cost']
        newTime = label.resourceDict['time'] + g[edge[0]][edge[1]]['time']
        
        newResDict = { 'cost' : newCost, 'time' : newTime }
        feasible = True
        
        return (feasible, rcsp_networkx.Label(edge[1], 
                                         edge, label, newResDict, labelNum))
        
    g = networkx.DiGraph()
    
    #===========================================================================
    # g.add_node("A", earliestTime = 0, latestTime = 0)
    # g.add_node("B", earliestTime = 5, latestTime = 20)
    # g.add_node("C", earliestTime = 6, latestTime = 10)
    # g.add_node("D", earliestTime = 3, latestTime = 12)
    # g.add_node("E", earliestTime = 0, latestTime = 100)
    #===========================================================================

    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")
    
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