'''
Created on 11/feb/2013

@author: sambarza@gmail.com
'''
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import BitMask32

class MouseOnInfo():
    
    def __init__(self, thing, thingId, node, nodeId, mouse_x, mouse_y):
        
        self.thing = thing
        self.thingId = thingId
        self.node = node
        self.nodeId = nodeId
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        
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
        
    def getMouseOn(self, mouse_x, mouse_y):
        
        #Set the position of the ray based on the mouse position
        self.pickerRay.setFromLens(self.camNode, mouse_x, mouse_y)
      
        self.picker.traverse(self.things.node)
        
        if self.pq.getNumEntries() > 0:
            #if we have hit something, sort the hits so that the closest
            #is first, and highlight that node
            self.pq.sortEntries()
            
            selectedNode = self.pq.getEntry(0).getIntoNode()
            
            selectedNodeId = selectedNode.getTag('nodeId')
            thingId        = selectedNode.getTag('ID')
            
            mouseOnInfo = MouseOnInfo(self.things.getById(thingId), thingId, selectedNode, selectedNodeId, mouse_x, mouse_y)
             
            return mouseOnInfo
                                        