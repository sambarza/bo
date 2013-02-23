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
    
    SWITCH_OFF = "SWITCH_OFF"
    SWITCH_ON = "SWITCH_ON"
    
    def __init__(self, ywn):
        '''
        Constructor
        '''
        Thing.__init__(self, "Lightswitch", ywn)
        
        self.model = loader.loadModel('models/Lightswitch')
        
        self.model.find("**/Piattina").node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find("**/Piattina").node().setTag('ID', self.Id)
        self.model.find("**/Piattina").node().setTag('nodeId', "Piattina")
        
        self.model.find("**/Switch").node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find("**/Switch").node().setTag('ID', self.Id)
        self.model.find("**/Switch").node().setTag('nodeId', "Switch")
        self.model.find("**/Switch").setP(332)
        
        self.model.find("**/TopScrew").node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find("**/TopScrew").node().setTag('ID', self.Id)
        self.model.find("**/TopScrew").node().setTag('nodeId', "TopScrew")
   
        self.model.find("**/BottomScrew").node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find("**/BottomScrew").node().setTag('ID', self.Id)
        self.model.find("**/BottomScrew").node().setTag('nodeId', "BottomScrew")
        
        self.model.setTag('ID', self.Id)
        
        self.status = Lightswitch.SWITCH_OFF
        
    def request(self, request):
        
        pass
    
    def switchOn(self):
        
        self.status = Lightswitch.SWITCH_ON
        
        self.setNewSwitchPosition(384)
                
        self.ywn.render.setLight(self.ywn.plnp)
        self.ywn.render.setLight(self.ywn.plnp5)

    def switchOff(self):
        
        self.status = Lightswitch.SWITCH_OFF
        
        self.setNewSwitchPosition(332)

        self.ywn.render.clearLight(self.ywn.plnp)
        self.ywn.render.clearLight(self.ywn.plnp5)

    def onLeftMouseClick(self):
        
        if self.status == Lightswitch.SWITCH_ON:
            self.switchOff()
        else:
            self.switchOn()
            
        self.updateTooltip()
        
    def onMouseHoverIn(self, previousThing, mouseOnInfo):
        self.lightsOn()
           
    def onMouseHoverOut(self, newThing):
        self.lightsOff()
        
    def setNewSwitchPosition(self, newPositionDegree):
        
        switch = self.model.find("**/Switch")
        
        h = switch.getH()
        p = newPositionDegree
        r = switch.getR()
        
        interval = LerpHprInterval(self.model.find("**/Switch"), 0.1, Vec3(h,p,r), blendType='easeInOut')
        interval.start()
        
    def getDefaultAction(self):
        
        if self.status == Lightswitch.SWITCH_ON:
            return "Switch Lights Off"
        elif self.status == Lightswitch.SWITCH_OFF:
            return "Switch Lights On"
