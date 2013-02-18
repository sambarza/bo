'''
Created on 13/feb/2013

@author: sambarza@gmail.com
'''

from pandac.PandaModules import BitMask32
from pandac.PandaModules import Vec3

from interval.LerpInterval import LerpHprInterval

from ywnThing import Thing

class Lightswitch(Thing):
    '''
    classdocs
    '''
    
    def __init__(self, ywn):
        '''
        Constructor
        '''
        Thing.__init__(self, "Lightswitch", ywn)
        
        self.model = loader.loadModel('models/Lightswitch')
        
        self.model.find("**/Piattina").node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find("**/Piattina").node().setTag('ID', self.Id)
        
        self.model.find("**/Switch").node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find("**/Switch").node().setTag('ID', self.Id)
        self.model.find("**/Switch").setP(332)
        
        self.model.find("**/TopScrew").node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find("**/TopScrew").node().setTag('ID', self.Id)
   
        self.model.find("**/BottomScrew").node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find("**/BottomScrew").node().setTag('ID', self.Id)
        
        self.model.setTag('ID', self.Id)
        
    def request(self, request):
        
        if self.fsm.state == self.fsm.AtHome or self.fsm.state == self.fsm.AtHomeWithLightsOn:
            
            Thing.request(self, request)
            
        pass
        
    def leftMouseClick(self):
        
        #if self.fsm.state != self.fsm.AtDeskWithFocus:
            
        #    return
        
        switch = self.model.find("**/Switch")
        
        h = switch.getH()
        p = switch.getP()
        r = switch.getR()
        
        if p == 332:
            p = 384
            self.ywn.render.clearLight(self.ywn.plnp)
            self.ywn.render.clearLight(self.ywn.plnp5)

        else:
            p = 332
            self.ywn.render.setLight(self.ywn.plnp)
            self.ywn.render.setLight(self.ywn.plnp5)

            
        interval = LerpHprInterval(self.model.find("**/Switch"), 0.1, Vec3(h,p,r), blendType='easeInOut')
        interval.start()
        