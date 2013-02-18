'''
Created on 14/feb/2013

@author: barzaghis
'''

from Events import Events

class EventHandler(object):
    '''
    classdocs
    '''

    def __init__(self, ywn):
        '''
        Constructor
        '''
        self.ywn = ywn
        
        self.ywn.accept('mouse1-up',self.eventLeftMouseUp)
        self.ywn.accept('mouse3-up',self.eventRightMouseUp)
        
    def eventLeftMouseUp(self):
        
        if self.ywn.mouseOn:
            print "Left Mouse on " + self.ywn.mouseOn.getThingName() + " " + self.ywn.mouseOn.Id
            self.ywn.mouseOn.request(Events.leftMouseClick)
            self.ywn.mouseOn.leftMouseClick()

    def eventRightMouseUp(self):
                   
        print "Right Mouse"
            
        if self.ywn.mouseOn:
            self.ywn.mouseOn.request(Events.rightMouseClick)

        self.ywn.camera.goHome()
            
    def eventMouseOnNewThing(self, previousThing, newThing):
        
        print "eventMouseOnNewThing", previousThing, newThing
        
        if previousThing:
            previousThing.request(Events.mouseOnOthers)
            
        if newThing:
            
            if newThing.canGetFocus:
                newThing.request(Events.mouseOnYou)
            else:
                self.ywn.tooltip.clearText()
                
        else:
            self.ywn.tooltip.clearText()
    
    def cameraGoingHome(self):
        
        print "cameraGoingHome"
        
        if self.ywn.focusOn != None:
            self.ywn.focusOn.request(Events.cameraGoingHome)
        
        self.ywn.focusOn = None
    
    def cameraGoingToThing(self, thing):
        
        print "cameraGoingToThing"
        
        if self.ywn.focusOn != None:
            self.ywn.focusOn.request(Events.focusRequestedByOthers)
        
        self.ywn.focusOn = None
        
    def cameraArrivedAtThing(self, thing):
        
        print "cameraArrivedAtThing"
        
        thing.request(Events.cameraArrivedToYou)
        
        self.ywn.setFocusOn(thing)
        
    def cameraDeviated(self, thing):
        
        print "cameraDeviated"
        
        thing.request(Events.cameraDeviated)