'''
Created on 13/feb/2013

@author: barzaghis
'''

from ywnThing import Thing
from pandac.PandaModules import BitMask32

class Book(Thing):
    '''
    classdocs
    '''
    
    ThingName = "Book"
    
    def __init__(self, ywn):
        '''
        Constructor
        '''
        Thing.__init__(self, "Book", ywn)
        
        self.model = loader.loadModel('models/Book')
        
        self.model.find("**/Front").node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find("**/Back").node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find("**/Front").node().setTag('ID', self.Id)
        self.model.find("**/Back").node().setTag('ID', self.Id)
        
        self.model.setTag('ID', self.Id)
        
    def getDefaultAction(self):
        
        return "Read"