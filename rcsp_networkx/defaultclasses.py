#===============================================================================
# Default Classes
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
        Parameters: resVert : Vertex
                    predEdge : Edge
                    predLabel : Label
                    resDict : Dictionary
                    labelID : Integer
         
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
#===============================================================================