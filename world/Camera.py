'''
Created on 11/feb/2013

@author: sambarza@gmail.com
'''

from pandac.PandaModules import Vec3

from direct.interval.LerpInterval import LerpHprInterval
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.IntervalGlobal import Sequence
from direct.interval.IntervalGlobal import Parallel
from direct.interval.IntervalGlobal import Func

class Camera(object):
    '''
    classdocs
    '''
    
    STATE_MOVING_TO_THING = 'STATE_MOVING_TO_THING'
    STATE_MOVING_TO_HOME = 'STATE_MOVING_TO_HOME'
    STATE_TURNING = 'STATE_TURNING'
    STATE_STILL_AT_HOME = 'STATE_STILL_AT_HOME' 
    STATE_STILL_AT_THING = 'STATE_STILL_AT_THING'
    STATE_STILL = 'STATE_STILL'
    
    def __init__(self, render, camera, eventHandler):
        '''
        Constructor
        '''
        
        self.camera = camera
        
        self.eventHandler = eventHandler
        
        self.followerCamera = render.attachNewNode("followerCamera")
        
        self.state = Camera.STATE_STILL_AT_HOME
        self.movingInterval = None
        self.lookingAt = None
        self.movingTo = None
        
        self.cameraOriginalPos = Vec3(0.00, -17.00, 8.00)
        self.cameraOriginalHpr = Vec3(0,0,0)
        
        self.duration = 0.50
        self.multi = 1.25
        self.lastDegree = 0
        
    def goHome(self):
        
        if self.state == Camera.STATE_MOVING_TO_HOME:
            return
        
        self.concludeCurrentMovement()

        self.followerCamera.setPos(self.cameraOriginalPos)
        self.followerCamera.setHpr(self.cameraOriginalHpr)
        
        intervalHpr = LerpHprInterval(self.camera, 0.7, self.followerCamera.getHpr(), blendType='easeInOut')
        intervalPos = LerpPosInterval(self.camera, 0.7, self.followerCamera.getPos(), blendType='easeInOut')

        self.movingInterval = Sequence( Parallel(intervalHpr, intervalPos, name="MovingCamera"), Func(self.arrivedAtHome))
        
        self.movingInterval.start()
        
        self.state = Camera.STATE_MOVING_TO_HOME

        self.lookingAtNothing()
        
        self.eventHandler.cameraGoingHome()
        
    def lookingAtNothing(self):
        
        self.lookingAt = None
        
    def arrivedAtHome(self):
        
        self.state = Camera.STATE_STILL_AT_HOME
        
    def lookAt(self, thing):
        
        self.concludeCurrentMovement()
            
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
        
        self.interv1 = LerpHprInterval(self.camera, duration, self.followerCamera.getHpr(), blendType='easeInOut')
        self.interv2 = LerpPosInterval(self.camera, duration, self.followerCamera.getPos(), blendType='easeInOut')
        
        self.movingInterval = Sequence(Parallel(self.interv2, self.interv1, name="Parallel Name1"), Func(self.arrivedAtThing))
               
        self.movingInterval.start()
        
        self.state = Camera.STATE_MOVING_TO_THING
                
        if self.camera.getH() == 360:
            self.camera.setH(0)
        
        self.eventHandler.cameraGoingToThing(self.movingTo)
        
    def arrivedAtThing(self):
        
        self.state     = Camera.STATE_STILL_AT_THING
        self.lookingAt = self.movingTo 
        self.movingTo  = None
        
        self.eventHandler.cameraArrivedAtThing(self.lookingAt)
        
    def turnFinished(self):
        
        self.state = Camera.STATE_STILL
        self.movingInterval = None
        
        self.duration = 0.50
        self.multi = 1.25
        self.lastDegree = 0
        
    def turn(self, deltaDegree):
        
        self.duration = 0.50
        
        if (self.lastDegree < 0 and deltaDegree > 0) or (self.lastDegree > 0 and deltaDegree < 0):
            self.multi = 1.25
             
        if self.state == Camera.STATE_TURNING:
            
            self.multi = self.multi + 0.25 
            deltaDegree = deltaDegree * self.multi
            
        self.concludeCurrentMovement()
        
        newH = self.camera.getH() + deltaDegree
        
        self.followerCamera.setH(newH)
        
        self.movingInterval = Sequence(LerpHprInterval(self.camera, self.duration, self.followerCamera.getHpr(), blendType='easeOut'), Func(self.turnFinished))
        self.movingInterval.start()

        self.lastDegree = deltaDegree
        self.state = Camera.STATE_TURNING
        self.lookingAtNothing()
        
    def lookLeft(self):
        
        self.turn(+5)
        
    def lookRight(self):
        
        self.turn(-5)
        
    def concludeCurrentMovement(self):
        
        if self.state == Camera.STATE_TURNING:
            
            self.movingInterval.pause()
            self.movingInterval = None
            
        if self.state == Camera.STATE_MOVING_TO_THING:
            
            self.movingInterval.pause()
            self.movingInterval = None
            
            self.eventHandler.cameraDeviated(self.movingTo)
            
            self.movingTo = None
            
        if self.state == Camera.STATE_MOVING_TO_HOME:
            
            self.movingInterval.pause()
            self.movingInterval = None
