'''
Created on 11/feb/2013

@author: sambarza@gmail.com
'''
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import BitMask32

class Picker(object):
    '''
    classdocs
    '''

    def __init__(self, camera, mouseWatcherNode, camNode, things):
        '''
        Constructor
        '''
        
        self.mouseWatcherNode = mouseWatcherNode
        self.camNode = camNode
        self.things = things
        
        self.pickerRay = CollisionRay()
        
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNode.setFromCollideMask(BitMask32.bit(1))
        self.pickerNode.addSolid(self.pickerRay)
        
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pq       = CollisionHandlerQueue()      
        
        self.picker = CollisionTraverser()
        self.picker.addCollider(self.pickerNP, self.pq)
        
    def getMouseOn(self):
        
        #Check to see if we can access the mouse. We need it to do anything else
        if not self.mouseWatcherNode.hasMouse():
            
            return None

        #get the mouse position
        mpos = self.mouseWatcherNode.getMouse()

        mouse_x = mpos.getX()
        mouse_y = mpos.getY()
        
        #Set the position of the ray based on the mouse position
        self.pickerRay.setFromLens(self.camNode, mouse_x, mouse_y)
      
        self.picker.traverse(self.things.node)
        
        if self.pq.getNumEntries() > 0:
            #if we have hit something, sort the hits so that the closest
            #is first, and highlight that node
            self.pq.sortEntries()

            thing_id = self.pq.getEntry(0).getIntoNode().getTag('ID')
            
            return self.things.getById(thing_id)
                                        