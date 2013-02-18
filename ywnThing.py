'''
Created on 10/feb/2013

@author: barzaghis
'''

from showbase import Loader
from direct.interval.LerpInterval import LerpColorScaleInterval
from pandac.PandaModules import Vec4

from ywnThingFsm import ywnThingFsm
from world.Camera import Camera

class Thing(object):
    '''
    classdocs
    '''
    lastId = 0
    
    def __init__(self, thingName, ywn):
        '''
        Constructor
        '''
        Thing.lastId = Thing.lastId + 1
        
        self.ywn = ywn
        self.Id = str(Thing.lastId)
        self.thingName = thingName
        self.lookFrom = None
        self.canGetFocus = True
        
        self.fsm = ywnThingFsm(self)

    def getThingInfo(self):
        
        return self.getThingName() + " id " + self.Id
    
    def setLookFrom(self, lookFrom):
        
        self.lookFrom = lookFrom
        
    def getLookFrom(self):
        
        return self.lookFrom
                
    def reparentTo(self, node):
        
        self.model.reparentTo(node)
        
    def setPosHprScale(self, X, Y, Z, H, P, R, SX, SY, SZ):
                       
        self.model.setPosHprScale(X, Y, Z, H, P, R, SX, SY, SZ)
        
    def getThingName(self):
        
        return self.thingName
    
    def request(self, request):
        
        self.fsm.request(request)
        
    def getDefaultAction(self):
        
        return "Nothing to do with"
    
    def lightsOn(self):
        
        lighting = LerpColorScaleInterval(self.model, 0.1, Vec4(5,5,5,1), blendType ='easeIn')
        lighting.start()
        
        self.ywn.tooltip.setText(self.getDefaultAction() + " " + self.getThingName() + " " + self.Id)
        
    def lightsOff(self):
        
        delighting = LerpColorScaleInterval(self.model, 0.1, Vec4(0.5,0.5,0.5,1), blendType ='easeOut')
        delighting.start()
        
        self.ywn.tooltip.clearText()
        
    def requestFocus(self):
        
        print self.getThingInfo() + " focus requested"
        
        self.ywn.camera.lookAt(self)
        
    def gotFocus(self):
        
        print self.getThingInfo() + " got focus"
        
    def leftMouseClick(self):
        
        pass