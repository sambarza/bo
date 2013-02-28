'''
Created on 13/feb/2013

@author: sambarza@gmail.com
'''

from ywnThing import Thing
from pandac.PandaModules import BitMask32

from direct.interval.LerpInterval import LerpColorScaleInterval
from pandac.PandaModules import Vec4

class Button():
    
    def __init__(self, id, model, nodeName):
        
        nodeRegEx = "**/" + nodeName
        
        self.nodeName = nodeName
        self.nodePath = model.find(nodeRegEx)
        self.node = self.nodePath.node()
        
        self.node.setIntoCollideMask(BitMask32.bit(1))
        self.node.setTag('ID', id)
        self.node.setTag('nodeId', nodeName)
        
        self.lighting = None
        
    def mouseHoverIn(self):
        
        if self.lighting != None:
            self.lighting.pause()

        self.lighting = LerpColorScaleInterval(self.nodePath, 0.1, Vec4(0.1,0.1,0.1,2), blendType ='noBlend')
        self.lighting.start()
        
    def mouseHoverOut(self):
        
        self.lighting = LerpColorScaleInterval(self.nodePath, 1.5, Vec4(0.5,0.5,0.5,1), blendType ='easeOut')
        self.lighting.start()       
        
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

        self.currentButton = None
        self.previousButton = None
        
        self.model = loader.loadModel('models/calculator/calculator')
        
        self.buttons = dict()
        
        self.buttons["base"] = Button(self.Id, self.model, "base")
        self.buttons["Zero"] = Button(self.Id, self.model, "Zero")
        self.buttons["Log"] = Button(self.Id, self.model, "Log")
        self.buttons["Four"] = Button(self.Id, self.model, "Four")
        self.buttons["Decimal"] = Button(self.Id, self.model, "Decimal")
        self.buttons["Divide"] = Button(self.Id, self.model, "Divide")
        self.buttons["Plus"] = Button(self.Id, self.model, "Plus")
        self.buttons["Seven"] = Button(self.Id, self.model, "Seven")
        self.buttons["Two"] = Button(self.Id, self.model, "Two")
        self.buttons["One"] = Button(self.Id, self.model, "One")
        self.buttons["Screen"] = Button(self.Id, self.model, "Screen")
        self.buttons["ClearEntry"] = Button(self.Id, self.model, "ClearEntry")
        self.buttons["Nine"] = Button(self.Id, self.model, "Nine")
        self.buttons["Pi"] = Button(self.Id, self.model, "Pi")
        self.buttons["On"] = Button(self.Id, self.model, "On")
        self.buttons["Three"] = Button(self.Id, self.model, "Three")
        self.buttons["Six"] = Button(self.Id, self.model, "Six")
        self.buttons["Eight"] = Button(self.Id, self.model, "Eight")
        self.buttons["Five"] = Button(self.Id, self.model, "Five")
        self.buttons["Minus"] = Button(self.Id, self.model, "Minus")
        self.buttons["Equals"] = Button(self.Id, self.model, "Equals")
        self.buttons["Multiply"] = Button(self.Id, self.model, "Multiply")
        
        self.model.setTag('ID', self.Id)
        
    def getDefaultAction(self):
        
        return "Press Me"
    
    def getButton(self, mouseOnInfo):
        
        return self.buttons[mouseOnInfo.nodeId]
        
    def onLeftMouseUp(self, mouseOnInfo):
        
        Thing.onLeftMouseUp(self, mouseOnInfo)
        
        if mouseOnInfo != None:
            print mouseOnInfo.nodeId
        
    def onMouseMoving(self, mouseOnInfo, previousMouseOnInfo):
        
        Thing.onMouseMoving(self, mouseOnInfo, previousMouseOnInfo)
        
        if self.fsm.state != self.fsm.AtHomeWithFocus:
            return
        
        if mouseOnInfo.nodeId == "base":
            
            self.previousButton = self.currentButton

            if self.currentButton != None:

                self.currentButton.mouseHoverOut()
                
                self.currentButton = None
            
            return

        self.previousButton = self.currentButton
        
        self.currentButton = self.getButton(mouseOnInfo)
        
        if self.currentButton == self.previousButton:
            return
                
        if self.previousButton != None:
            self.previousButton.mouseHoverOut()
        
        self.currentButton.mouseHoverIn()
        
    def onMouseHoverOut(self, newThing):
        
        Thing.onMouseHoverOut(self, newThing)
        
        if self.currentButton != None:
            self.currentButton.mouseHoverOut()
        
        self.currentButton = None
        self.previousButton = None