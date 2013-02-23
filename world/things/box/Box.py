'''
Created on 13/feb/2013

@author: sambarza@gmail.com
'''

from ywnThing import Thing
from pandac.PandaModules import BitMask32

class Box(Thing):
    '''
    classdocs
    '''
    
    def __init__(self, ywn):
        '''
        Constructor
        '''
        Thing.__init__(self, "Box", ywn)
        
        self.model = loader.loadModel('models/untitled2')
        
        self.model.find("**/Cube").node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find("**/Cube").node().setTag('ID', self.Id)
        self.model.find("**/Cube").node().setTag('nodeId', "cube")
        
        self.model.setTag('ID', self.Id)