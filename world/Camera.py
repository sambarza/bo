'''
Created on 11/feb/2013

@author: sambarza@gmail.com
'''

from pandac.PandaModules import Vec3

from interval.LerpInterval import LerpHprInterval, LerpPosInterval
from direct.interval.IntervalGlobal import Sequence
from direct.interval.IntervalGlobal import Parallel
from direct.interval.IntervalGlobal import Func

class Camera(object):
    '''
    classdocs
    '''
    
    STATE_MOVING_TO_THING = 'STATE_MOVING_TO_THING'
    STATE_MOVING_TO_HOME = 'STATE_MOVING_TO_HOME'
    STATE_STILL_AT_HOME = 'STATE_STILL_AT_HOME' 
    STATE_STILL_AT_THING = 'STATE_STILL_AT_THING'
    
    def __init__(self, render, camera, eventHandler):
        '''
        Constructor
        '''
        
        self.camera = camera
        self.eventHandler = eventHandler
        
        self.followerCamera = render.attachNewNode("followerCamera")
        
        self.state = self.STATE_STILL_AT_HOME
        self.movingInterval = None
        self.lookingAt = None
        self.movingTo = None
        
        self.cameraOriginalPos = Vec3(0.00, -17.00, 8.00)
        self.cameraOriginalHpr = Vec3(0,0,0)
        
    def goHome(self):
        
        print "Camera go home!"
        
        if self.state == self.STATE_MOVING_TO_THING:
            self.movingInterval.pause()
            self.movingInterval = None
           
            self.eventHandler.cameraDeviated(self.movingTo)

            self.movingTo = None
            
        if self.state == self.STATE_MOVING_TO_HOME:
            return
            
        self.followerCamera.setPos(self.cameraOriginalPos)
        self.followerCamera.setHpr(self.cameraOriginalHpr)
        
        intervalHpr = LerpHprInterval(self.camera, 0.7, self.followerCamera.getHpr(), blendType='easeInOut')
        intervalPos = LerpPosInterval(self.camera, 0.7, self.followerCamera.getPos(), blendType='easeInOut')

        self.movingInterval = Sequence( Parallel(intervalHpr, intervalPos, name="MovingCamera"), Func(self.arrivedAtHome))
        
        self.movingInterval.start()
        
        self.state = self.STATE_MOVING_TO_HOME
        self.lookingAt = None
        
        self.eventHandler.cameraGoingHome()
        
    def arrivedAtHome(self):
        
        print "Camera arrived at home"
        
        self.state = self.STATE_STILL_AT_HOME
        
    def lookAt(self, thing):
        
         
        if self.state == self.STATE_MOVING_TO_THING:
            
            self.movingInterval.pause()
            self.movingInterval = None
            
            self.eventHandler.cameraDeviated(self.movingTo)
            
        if self.state == self.STATE_MOVING_TO_HOME:
            
            self.movingInterval.pause()
            self.movingInterval = None
                
        model = thing.model
        self.movingTo = thing
        
        lookFrom = thing.getLookFrom()

        if lookFrom == 'E':
            
            self.followerCamera.setX(model.getX() + 6)
            self.followerCamera.setY(model.getY())
            self.followerCamera.setZ(model.getZ() + 2)
            
        elif lookFrom == 'W':

            self.followerCamera.setX(model.getX() - 6)
            self.followerCamera.setY(model.getY())
            self.followerCamera.setZ(model.getZ() + 2)

        elif lookFrom == 'S':
            
            self.followerCamera.setX(model.getX())
            self.followerCamera.setY(model.getY() - 6)
            self.followerCamera.setZ(model.getZ() + 2)
            
        elif lookFrom == 'N':
            
            self.followerCamera.setX(model.getX())
            self.followerCamera.setY(model.getY() + 6)
            self.followerCamera.setZ(model.getZ() + 2)
            
        self.followerCamera.lookAt(model)
        self.followerCamera.setP(self.followerCamera.getP() + 10)
        
        print "AttualeAt " + str(self.camera.getHpr())
        print "LookAt " + str(self.followerCamera.getHpr())
        
        if self.camera.getH() == -90 and self.followerCamera.getH() == 180:
            self.followerCamera.setH(-180)
        
        if self.camera.getH() == 180 and self.followerCamera.getH() == -90:
            self.followerCamera.setH(270)
            
        if self.camera.getH() == 270 and self.followerCamera.getH() == -90:
            self.followerCamera.setH(270)
            
        if self.camera.getH() == -180 and self.followerCamera.getH() == 90:
            self.followerCamera.setH(90)
            
        if self.camera.getH() == -90 and self.followerCamera.getH() == 90:
            self.followerCamera.setH(90)
        
        if self.camera.getH() == 180 and self.followerCamera.getH() == 0:
            self.followerCamera.setH(360)
        
        if self.camera.getH() == 0 and self.followerCamera.getH() == 180:
            self.followerCamera.setH(-180)
        
        distance = self.camera.getDistance(self.followerCamera) 
        speed = 5
        duration = distance * speed / 100
         
        if duration < 1:
            duration = 1
        
        print "Distance from camera to thing " + str(distance)
        print "Duration " + str(duration)
        
        self.interv1 = LerpHprInterval(self.camera, duration, self.followerCamera.getHpr(), blendType='easeInOut')
        self.interv2 = LerpPosInterval(self.camera, duration, self.followerCamera.getPos(), blendType='easeInOut')
        
        self.movingInterval = Sequence(Parallel(self.interv2, self.interv1, name="Parallel Name1"), Func(self.arrivedAtThing))
               
        self.movingInterval.start()
        
        self.state = self.STATE_MOVING_TO_THING
                
        if self.camera.getH() == 360:
            self.camera.setH(0)
        
        self.eventHandler.cameraGoingToThing(self.movingTo)
        
    def arrivedAtThing(self):
        
        print "Camera arrived at thing " + self.movingTo.getThingInfo()
        
        self.state     = self.STATE_STILL_AT_THING
        self.lookingAt = self.movingTo 
        self.movingTo  = None
        
        self.eventHandler.cameraArrivedAtThing(self.lookingAt)
        
