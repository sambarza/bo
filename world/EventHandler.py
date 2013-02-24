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

        self.ywn.accept('mouse1',self.eventLeftMouseDown)
        self.ywn.accept('mouse1-up',self.eventLeftMouseUp)
        
        self.ywn.accept('mouse3-up',self.eventRightMouseUp)
        self.ywn.accept('wheel_up',self.scrollLeft)
        self.ywn.accept('wheel_down',self.scrollRight)
        self.ywn.accept("escape", sys.exit, [0])
        
    def scrollLeft(self):
        
        self.ywn.camera.lookLeft()
        
    def scrollRight(self):
        
        self.ywn.camera.lookRight()

    def eventLeftMouseDown(self):
               
        if self.ywn.mouseWatcher.mouseOnInfo:
            self.ywn.mouseWatcher.mouseOnInfo.thing.onLeftMouseDown(self.ywn.mouseWatcher.mouseOnInfo)
            
    def eventLeftMouseUp(self):
               
        if self.ywn.mouseWatcher.mouseOnInfo:
            self.ywn.mouseWatcher.mouseOnInfo.thing.onLeftMouseUp(self.ywn.mouseWatcher.mouseOnInfo)

    def eventRightMouseUp(self):
                   
        if self.ywn.mouseWatcher.mouseOnInfo:
            self.ywn.mouseWatcher.mouseOnInfo.thing.onRightMouseClick()
            
        self.ywn.camera.goHome()

    def eventMouseOnNewThing(self, previousThing, newThing, mouseOnInfo):
        
        if previousThing:
            previousThing.onMouseHoverOut(newThing)
            
        if newThing and newThing.canGetMouseHover():
            newThing.onMouseHoverIn(previousThing, mouseOnInfo)
    
    def eventMouseMovingOnThing(self, mouseOn, mouseOnInfo, previousMouseOnInfo):
        
        if mouseOn != None:
            mouseOn.onMouseMoving(mouseOnInfo, previousMouseOnInfo)

    def cameraGoingHome(self):
        
        if self.ywn.focusOn != None:
            self.ywn.focusOn.onCameraGoingHome()
        
        self.ywn.focusOn = None
    
    def cameraGoingToThing(self, thing):
        
        if self.ywn.focusOn != None:
            self.ywn.focusOn.request(Events.focusRequestedByOthers)
        
        self.ywn.focusOn = None
        
    def cameraArrivedAtThing(self, thing):
        
        thing.request(Events.cameraArrivedToYou)
        
        self.ywn.setFocusOn(thing)
        
    def cameraDeviated(self, thing):
        
        thing.request(Events.cameraDeviated)