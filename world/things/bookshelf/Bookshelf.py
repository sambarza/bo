'''
Created on 13/feb/2013

@author: sambarza@gmail.com
'''

from ywnThing import Thing
from pandac.PandaModules import BitMask32

class Bookshelf(Thing):
    '''
    classdocs
    '''
    
    def __init__(self, ywn):
        '''
        Constructor
        '''
        Thing.__init__(self, "Bookshelf", ywn)
        
        self.model = loader.loadModel('models/BookShelf')
        
        self.model.find("**/BookShelf").node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find("**/BookShelf").node().setTag('ID', self.Id)
        
        self.model.setTag('ID', self.Id)
        
        self.canGetFocus = False
    
    def lightsOn(self):
        
        self.ywn.tooltip.setText("I' only a bookshelf!")
        
    def lightsOff(self):
        
        pass
        
    def request(self, request):
        
        return
    
        