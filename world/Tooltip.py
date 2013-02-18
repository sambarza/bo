'''
Created on 13/feb/2013

@author: barzaghis
'''

from pandac.PandaModules import TextNode

class Tooltip(object):
    '''
    classdocs
    '''


    def __init__(self, ywn):
        '''
        Constructor
        '''
        
        self.ywn = ywn
        
        self.tooltip = TextNode('Tooltip')
        self.tooltip.setText("Every day in every way I'm getting better and better.")
        self.tooltip.setTextColor(1, 0.5, 0.5, 1)
        self.tooltip.setShadow(0.05, 0.05)
        self.tooltip.setShadowColor(0, 0, 0, 1)
        self.tooltipNodePath = self.ywn.aspect2d.attachNewNode(self.tooltip)
        self.tooltipNodePath.setScale(0.07)
        self.tooltipNodePath.setPos(-1,0,0.9)
        
        self.ywn.taskMgr.add(self.taskMouseTooltip, 'taskMouseToolip')
        
    def setText(self, text):
        
        self.tooltip.setText(text)
        
    def clearText(self):
        
        self.tooltip.clearText()
        
    def taskMouseTooltip(self, task):
        
        self.tooltipNodePath.setPos(self.ywn.mouse_x * self.ywn.getAspectRatio(), 0, self.ywn.mouse_y)
        
        #if self.ywn.previousMouseOn == self.ywn.mouseOn:
        #    return task.cont
        
        #if self.ywn.mouseOn != None:
        #    
        #    if self.ywn.mouseOn.fsm.state == None:
        #        stato = self.ywn.mouseOn.fsm.oldState + "->" + self.ywn.mouseOn.fsm.newState
        #    else:
        #        stato = self.ywn.mouseOn.fsm.state
        #        
        #    self.tooltip.setText(self.ywn.mouseOn.getThingName() + " " + self.ywn.mouseOn.Id + " Stato: " + stato)
        #else:
        #    self.tooltip.clearText()
        
        return task.cont