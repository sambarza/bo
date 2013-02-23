'''
Created on 23/feb/2013

@author: barzaghis
'''

class MouseWatcher(object):
    '''
    classdocs
    '''


    def __init__(self, taskMgr, eventHandler, picker):
        '''
        Constructor
        '''
        
        self.mouseOn = None
        self.mouseOnInfo = None
        
        self.previousMouseOn = None
        self.previousMouseOnInfo = None
        
        self.mouse_x = 0
        self.mouse_y = 0
        
        self.eventHandler = eventHandler
        
        self.picker = picker
        
        taskMgr.add(self.taskMouseOn, 'getMouseOn')
        
    def taskMouseOn(self, task):
        
        if not base.mouseWatcherNode.hasMouse():
            
            return task.cont
        
        self.previousMouseOnInfo = self.mouseOnInfo
        self.previousMouseOn = self.mouseOn
        self.mouseOn = None

        mpos = base.mouseWatcherNode.getMouse()
        
        self.mouse_x = mpos.getX()
        self.mouse_y = mpos.getY()
        
        self.mouseOnInfo = self.picker.getMouseOn(self.mouse_x, self.mouse_y)
        
        if self.mouseOnInfo:
            self.mouseOn = self.mouseOnInfo.thing
        
        if self.mouseOn <> self.previousMouseOn:
            self.eventHandler.eventMouseOnNewThing(self.previousMouseOn, self.mouseOn, self.mouseOnInfo)
            
        if self.mouseMoved(self.previousMouseOnInfo, self.mouseOnInfo) and self.mouseOn == self.previousMouseOn:
            self.eventHandler.eventMouseMovingOnThing(self.mouseOn, self.mouseOnInfo, self.previousMouseOnInfo)
            
        return task.cont
    
    def mouseMoved(self, previousMouseInfo, newMouseInfo):
        
        if previousMouseInfo == None:
            return False

        if newMouseInfo == None:
            return False
        
        if ( previousMouseInfo.mouse_x <> newMouseInfo.mouse_x ) or ( previousMouseInfo.mouse_y <> newMouseInfo.mouse_y ):
            return True
        else:
            return False