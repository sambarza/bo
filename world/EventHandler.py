'''
Created on 14/feb/2013

@author: sambarza@gmail.com
'''

from Events import Events
import sys

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
        self.ywn.accept('wheel_up',self.scrollLeft)
        self.ywn.accept('wheel_down',self.scrollRight)
        self.ywn.accept("escape", sys.exit, [0])
        
    def scrollLeft(self):
        
        self.ywn.camera.lookLeft()
        
    def scrollRight(self):
        
        self.ywn.camera.lookRight()

    def eventLeftMouseUp(self):
               
        if self.ywn.mouseOn:
            print "Left Mouse on " + self.ywn.mouseOn.getThingName() + " " + self.ywn.mouseOn.Id
            self.ywn.mouseOn.onLeftMouseClick()

    def eventRightMouseUp(self):
                   
        print "Right Mouse"
            
        if self.ywn.mouseOn:
            self.ywn.mouseOn.onRightMouseClick()
            
        self.ywn.camera.goHome()

    def eventMouseOnNewThing(self, previousThing, newThing, mouseOnInfo):
        
        print "eventMouseOnNewThing", previousThing, newThing
        
        if previousThing:
            previousThing.onMouseHoverOut(newThing)
            
        if newThing and newThing.canGetMouseHover():
            newThing.onMouseHoverIn(previousThing, mouseOnInfo)
    
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
        
    def eventMouseMovingOnThing(self, mouseOn, mouseOnInfo, previousMouseOnInfo):
        
        if mouseOn != None:
            mouseOn.onMouseMoving(mouseOnInfo, previousMouseOnInfo)