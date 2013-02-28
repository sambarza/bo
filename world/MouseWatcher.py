'''
Created on 23/feb/2013

@author: barzaghis
'''

class MousePosition(object):
    
    def __init__(self):
        
        self.x = 0
        self.y = 0
    
    def getCurrentPosition(self):
        
        mpos = base.mouseWatcherNode.getMouse()
        
        self.x = mpos.getX()
        self.y = mpos.getY()
    
    def copyFrom(self, position):
        
        self.x = position.x
        self.y = position.y
        
class MouseWatcher(object):
    '''
    classdocs
    '''


    def __init__(self, ywn, taskMgr, eventHandler, picker):
        '''
        Constructor
        '''
        
        self.mouseOn = None
        self.mouseOnInfo = None
        
        self.previousMouseOn = None
        self.previousMouseOnInfo = None
        
        self.currentPosition = MousePosition()
        self.previousPosition = MousePosition()
        
        self.eventHandler = eventHandler
        
        self.picker = picker
        
        ywn.accept('mouse1',self.leftMouseDown)
        ywn.accept('mouse1-up',self.leftMouseUp)
        
        ywn.accept('mouse3-up',self.rightMouseUp)
        ywn.accept('wheel_up',self.scrollLeft)
        ywn.accept('wheel_down',self.scrollRight)
        
        self.leftMouseIsDown = False
        self.leftMouseDownStartTime = None
        
        taskMgr.add(self.taskMouseOn, 'getMouseOn')
        
    def leftMouseDown(self):
        
        self.leftMouseDownStartTime = globalClock.getRealTime()
        self.leftMouseIsDown = True
        
        taskMgr.add(self.taskMouseLongLeftButton, 'getMouseContextMenu')
        taskMgr.add(self.taskMouseDrag, 'getMouseDrag')
        
        self.eventHandler.eventLeftMouseDown(self.mouseOnInfo)
        
    def leftMouseUp(self):
        
        self.leftMouseDownStartTime = None
        self.leftMouseIsDown = False
        
        taskMgr.remove('getMouseContextMenu')
        taskMgr.remove('getMouseDrag')
        
        self.eventHandler.eventLeftMouseUp()
        
    def rightMouseUp(self):
        
        self.eventHandler.eventRightMouseUp()
        
    def scrollLeft(self):
        
        self.eventHandler.eventScrollLeft()
        
    def scrollRight(self):
        
        self.eventHandler.eventScrollRight()
        
    def taskMouseOn(self, task):
        
        if not base.mouseWatcherNode.hasMouse():
            
            return task.cont
        
        self.previousMouseOnInfo = self.mouseOnInfo
        self.previousMouseOn = self.mouseOn
        self.mouseOn = None
        
        self.previousPosition.copyFrom(self.currentPosition)

        self.currentPosition.getCurrentPosition()
        
        self.mouseOnInfo = self.picker.getMouseOn(self.currentPosition.x, self.currentPosition.y)

        self.mouseIsMoved = self.mouseMoved(self.previousPosition, self.currentPosition)
        
        if self.mouseIsMoved:
            self.leftMouseDownStartTime = globalClock.getRealTime()
            
        if self.mouseOnInfo:
            self.mouseOn = self.mouseOnInfo.thing
        
        if self.mouseOn <> self.previousMouseOn:
            self.eventHandler.eventMouseOnNewThing(self.previousMouseOn, self.mouseOn, self.mouseOnInfo)
            
        if self.mouseIsMoved and self.mouseOn == self.previousMouseOn:
            self.eventHandler.eventMouseMovingOnThing(self.mouseOn, self.mouseOnInfo, self.previousMouseOnInfo)
            
        return task.cont
    
    def taskMouseDrag(self, task):
        
        if self.leftMouseIsDown and self.mouseIsMoved and self.mouseOn == self.previousMouseOn:
            print "Start drag"
            return task.done
        
        return task.cont
        
    def taskMouseLongLeftButton(self, task):
        
        currentTime = globalClock.getRealTime()
        currentButtonElapsed = currentTime - self.leftMouseDownStartTime
        
        if currentButtonElapsed >= 0.7:
            taskMgr.remove('getMouseDrag')
            self.eventHandler.eventLongLeftButtonDown(self.mouseOnInfo)
            return task.done
        
        return task.cont
    
    def mouseMoved(self, previousPosition, currentPosition):
        
        if ( previousPosition.x <> currentPosition.x ) or ( previousPosition.y <> currentPosition.y ):
            return True
        else:
            return False