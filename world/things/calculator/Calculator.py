'''
Created on 13/feb/2013

@author: sambarza@gmail.com
'''

from ywnThing import Thing
from pandac.PandaModules import BitMask32

from direct.interval.LerpInterval import LerpColorScaleInterval
from pandac.PandaModules import Vec4

class Calculator(Thing):
    '''
    classdocs
    '''
    
    ThingName = "Calculator"
    
    def __init__(self, ywn):
        '''
        Constructor
        '''
        Thing.__init__(self, "Calculator", ywn)
        self.button = None
        
        self.model = loader.loadModel('models/calculator/calculator')
        
        self.prepareNode("base")
        self.prepareNode("Zero")
        self.prepareNode("Log")
        self.prepareNode("Four")
        self.prepareNode("Decimal")
        self.prepareNode("Divide")
        self.prepareNode("Plus")
        self.prepareNode("Seven")
        self.prepareNode("Two")
        self.prepareNode("One")
        self.prepareNode("Screen")
        self.prepareNode("ClearEntry")
        self.prepareNode("Nine")
        self.prepareNode("Pi")
        self.prepareNode("On")
        self.prepareNode("Three")
        self.prepareNode("Six")
        self.prepareNode("Eight")
        self.prepareNode("Five")
        self.prepareNode("Minus")
        self.prepareNode("Equals")
        self.prepareNode("Multiply")
        
        self.model.setTag('ID', self.Id)
        
    def prepareNode(self, node):
        
        nodeRegEx = "**/" + node
        
        self.model.find(nodeRegEx).node().setIntoCollideMask(BitMask32.bit(1))
        self.model.find(nodeRegEx).node().setTag('ID', self.Id)
        self.model.find(nodeRegEx).node().setTag('nodeId', node)
        
    def getDefaultAction(self):
        
        return "Press Me"
    
    def getButton(self, mouseOnInfo):
        
        nodeRegEx = "**/" + mouseOnInfo.nodeId
        
        return self.model.find(nodeRegEx)
        
    def onMouseMoving(self, mouseOnInfo, previousMouseOnInfo):
        
        if self.fsm.state != self.fsm.AtHomeWithFocus:
            return
        
        if mouseOnInfo.nodeId == previousMouseOnInfo.nodeId:
            return
               
        if mouseOnInfo.nodeId == "base":
            delighting = LerpColorScaleInterval(self.getButton(previousMouseOnInfo), 0.1, Vec4(0.5,0.5,0.5,1), blendType ='noBlend')
            delighting.start()
            
            return
        
        delighting = LerpColorScaleInterval(self.getButton(previousMouseOnInfo), 0.1, Vec4(0.5,0.5,0.5,1), blendType ='noBlend')
        delighting.start()
            
        lighting = LerpColorScaleInterval(self.getButton(mouseOnInfo), 0.1, Vec4(0.1,0.1,0.1,2), blendType ='noBlend')
        lighting.start()
        
        self.button = mouseOnInfo
        
    def onMouseHoverOut(self, newThing):
        
        Thing.onMouseHoverOut(self, newThing)
        
        if self.button != None:
            delighting = LerpColorScaleInterval(self.getButton(self.button), 0.1, Vec4(0.5,0.5,0.5,1), blendType ='easeOut')
            delighting.start()
        
        self.button = None