# MouseControls.py
# Move the mouse pointer to the edge of the screen to rotate the camera.
# The Left and Right arrows also rotate the camera. The Mouse Wheel zooms the
# camera in and out. The Up and Down arrows also zoom the camera in and out.
# Move the player with the W, A, S, D keys.

def restrain(i, mn = -1, mx = 1): return min(max(i, mn), mx)

from showbase import Loader
from panda3d.core import loadPrcFileData
loadPrcFileData("", "want-directtools #t")
loadPrcFileData("", "want-tk #t")

from direct.gui.DirectGui import OnscreenText
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *

import direct.directbase.DirectStart
from direct.interval.IntervalGlobal import *
from interval.LerpInterval import * 
import sys

#!/usr/bin/python
'''

   First attempt at Panda3D.
   cblouin at cs dal ca
'''

# Import section

# Definitions
class World(DirectObject):
    def __init__(self):
        
        #PStatClient.connect()
        
        base.disableMouse()
        self.LoadHouse()

        # Lights
        self.LoadLight()

        self.movingCamera = None
        self.scrolling = False
        
        # Camera
        self.LoadCamera()
        
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNode.setFromCollideMask(BitMask32.bit(1))
        self.pickerRay = CollisionRay()               #Make our ray
        self.pickerNode.addSolid(self.pickerRay)      #Add it to the collision node
        
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        
        #Register the ray as something that can cause collisions
        self.picker = CollisionTraverser()            #Make a traverser
        self.pq     = CollisionHandlerQueue()         #Make a handler      
        self.picker.addCollider(self.pickerNP, self.pq)
        #self.picker.showCollisions(render)
        for i in range(6):
            self.box4[i].find("**/Cube").node().setIntoCollideMask(BitMask32.bit(1))
        
        self.dragging = False
        
        taskMgr.add(self.taskMouseDragging, 'taskMouseDragging')
        taskMgr.add(self.taskMouseToolip, 'taskMouseToolip')
        
        self.accept('mouse1',self.eventMouseDown)
        self.accept('mouse1-up',self.eventMouseUp)
        self.accept('mouse3',self.cameraGoHome)
        self.accept('wheel_up',self.scrollLeft)
        self.accept('wheel_down',self.scrollRight)
        self.accept('shift-wheel_up',self.scrollUp)
        self.accept('shift-wheel_down',self.scrollDown)
        self.accept("a", self.eventA)
        self.accept("escape", sys.exit, [0])
        
        self.interv = None
        self.ex_mpos_x = None
        self.ex_mpos_y = None
        self.lastMouseOn = None
        self.previousMouseOn = None
        self.box_current = self.box4[1]
        self.lookingAt = None
        self.done = False
        
        self.lookAtMode = 'A'
        
        self.tooltip = TextNode('node name')
        self.tooltip.setText("Every day in every way I'm getting better and better.")
        self.tooltipNodePath = aspect2d.attachNewNode(self.tooltip)
        self.tooltipNodePath.setScale(0.07)
        self.tooltipNodePath.setPos(-1,0,0.9)
        self.tooltip.setTextColor(1, 0.5, 0.5, 1)
        self.tooltip.setShadow(0.05, 0.05)
        self.tooltip.setShadowColor(0, 0, 0, 1)
        #self.tooltip.setCardColor(1, 1, 0.5, 1)
        #self.tooltip.setCardAsMargin(0, 0, 0, 0)
        #self.tooltip.setCardDecal(True)
        base.setFrameRateMeter(True)
        render.analyze()
        
    def eventA(self):
        
        if base.camera.getH() == 0:
            print base.camera.getH()
            base.camera.setH(360)
        else:
            print base.camera.getH()
            base.camera.setH(0)
        
    def movingMouse(self):

        #Check to see if we can access the mouse. We need it to do anything else
        if not base.mouseWatcherNode.hasMouse():
            
            return None

        mpos = base.mouseWatcherNode.getMouse()

        mouse_x = mpos.getX()
        mouse_y = mpos.getY()
        
        if mouse_x == self.ex_mpos_x and mouse_y == self.ex_mpos_y:
            
            moving = False
        
        else:
            moving = True
     
        self.ex_mpos_x = mouse_x
        self.ex_mpos_y = mouse_y
        
        return moving        

    def getMouseOn(self):
        
        #Check to see if we can access the mouse. We need it to do anything else
        if not base.mouseWatcherNode.hasMouse():
            
            return None

        #get the mouse position
        mpos = base.mouseWatcherNode.getMouse()

        mouse_x = mpos.getX()
        mouse_y = mpos.getY()
        
        self.lastMouseOn = None
        
        #self.tooltip.setText('Mouse X:' + str(mouse_x) + 'Y:' + str(mouse_y))
        self.tooltipNodePath.setPos(mouse_x * base.getAspectRatio(),0,mouse_y)
        
        #Set the position of the ray based on the mouse position
        self.pickerRay.setFromLens(base.camNode, mouse_x, mouse_y)
      
        self.picker.traverse(self.boxes)
        
        if self.pq.getNumEntries() > 0:
            #if we have hit something, sort the hits so that the closest
            #is first, and highlight that node
            self.pq.sortEntries()
            #print self.pq.getEntry(0).getIntoNode().getTag('box4')
            i = int(self.pq.getEntry(0).getIntoNode().getTag('box4'))
            
            self.lastMouseOn = self.box4[i]
             
            return self.box4[i]
    
    def eventMouseDown(self):
        
        print "Mouse Down"
        
        #if self.scrolling == True:
        #    print "Stop scroll"
            #self.interScrolling.pause()
        #    self.scrolling = False
        #    self.dragging = False
        #    return

        mpos = base.mouseWatcherNode.getMouse()
        
        self.draggingX = mpos.getX()
        print "Mouse X "+ str(self.draggingX) 

        #self.dragging = True        
        
    def eventMouseUp(self):
        
        self.dragging = False
        
        mouseOn = self.getMouseOn()
        
        if self.done != True and self.lookingAt != None and mouseOn == self.lookingAt:
            
            intervalPos = LerpPosInterval(self.lookingAt, 1.50, Vec3(2.50, 15.00, 6.70), blendType='easeOut')
            intervalHpr = LerpHprInterval(self.lookingAt, 1.50, Vec3(0.00, 270.00, 0.00), blendType='easeOut')
            interval = Parallel(intervalPos, intervalHpr, name="Parallel Name")
            
            apriLibro = LerpHprInterval(self.lookingAt.find("**/Back"), 0.50, Vec3(180.00, 0.00, 0.00), blendType='easeOut') 
            
            tutto = Sequence(interval, apriLibro)
            
            self.lookingAt.setTag("LookAtMeFrom","S")
            tutto.start()
            
            self.cameraGotoDesk()
            
            self.done = True
            
            return
            
        if mouseOn != None:
            self.cameraLookAt(mouseOn)
            self.setLightsOn(mouseOn)                      
        
    def cameraGotoDesk(self):
        
        self.followerCamera.setPosHprScale(2.00, 10.60, 12.70, 0.00, -49.00, 0.00, 1.00, 1.00, 1.00)
        
        self.interv1 = LerpHprInterval(base.camera, 0.50, self.followerCamera.getHpr(), blendType='easeInOut')
        self.interv2 = LerpPosInterval(base.camera, 0.50, self.followerCamera.getPos(), blendType='easeInOut')
        
        self.movingCamera = Parallel(self.interv2, self.interv1, name="Parallel Name1")
        
        self.movingCamera.start()

        
    def scrollLeft(self):
        
        h = base.camera.getH() + 15
        
        self.followerCamera.setH(h)
        
        self.interScrolling = LerpHprInterval(base.camera, 0.50, self.followerCamera.getHpr(), blendType='easeOut')
        self.interScrolling.start()
        print "Start scroll left"
        self.scrolling = True
        
    def scrollRight(self):
        
        h = base.camera.getH() - 15
        
        self.followerCamera.setH(h)
        
        self.interScrolling = LerpHprInterval(base.camera, 0.50, self.followerCamera.getHpr(), blendType='easeOut')
        self.interScrolling.start()
        print "Start scroll right"
        self.scrolling = True
        
    def scrollUp(self):
        
        h = base.camera.getP() + 15
        
        self.followerCamera.setP(h)
        
        self.interScrolling = LerpHprInterval(base.camera, 0.50, self.followerCamera.getHpr(), blendType='easeOut')
        self.interScrolling.start()
        print "Start scroll up"
        self.scrolling = True
        
    def scrollDown(self):
        
        h = base.camera.getP() - 15
        
        self.followerCamera.setP(h)
        
        self.interScrolling = LerpHprInterval(base.camera, 0.50, self.followerCamera.getHpr(), blendType='easeOut')
        self.interScrolling.start()
        print "Start scroll up"
        self.scrolling = True
        
    def startScrolling(self):
            
        mpos = base.mouseWatcherNode.getMouse()
        
#        velocita = abs(self.draggingX - mpos.getX()) * 100
#        if (velocita == 0):
#            velocita = 0.00001
        
        print "Scroll mouse X " + str(mpos.getX())
        
        if self.draggingX == mpos.getX():
            return

        if self.draggingX < mpos.getX():
            h = base.camera.getH() + (restrain(abs(self.draggingX - mpos.getX())) * 270)
        else:
            h = base.camera.getH() - (restrain(abs(self.draggingX - mpos.getX())) * 270)
            
        self.followerCamera.setH(h)
        
        self.interScrolling = LerpHprInterval(base.camera, 0.50, self.followerCamera.getHpr(), blendType='easeOut')
        self.interScrolling.start()
        print "Start scroll"
        self.scrolling = True
                      
        self.draggingX = mpos.getX()
                
    def taskMouseDragging(self, task):
        
        #print "dragging: " + str(self.dragging)
        
        if self.dragging and self.movingMouse():
            self.startScrolling()

        return task.cont

    def taskMouseToolip(self, task):
        
        mouseOn = self.getMouseOn()
        
        if self.previousMouseOn == mouseOn:
            return task.cont
        
        if mouseOn != None:
            self.tooltip.setText('Box: ' + mouseOn.getTag('box4') + "Label: " + mouseOn.getTag('label'))
            self.setLightsOn(mouseOn)
        else:
            self.tooltip.clearText()
        
        self.previousMouseOn = mouseOn
        
        return task.cont

    def LoadHouse(self):
        
        self.house = loader.loadModel('models/bedroom')
        self.house.reparentTo(render)
        self.house.setPosHprScale(0.00, 0.00, 0.00, 180.00, 0.00, 0.00, 1.26, 1.26, 1.26)
        
        #self.counter = loader.loadModel('models/abstractroom')
        #self.counter.reparentTo(render)
        #self.box2 = loader.loadModel('models/room2')
        #self.box2.reparentTo(render)
        #self.box2.setSx(0.0005)
        #self.box2.setSy(0.0005)
        #self.box2.setSz(0.0002)
        #self.box2.setPosHprScale(-34.30, 0.00, 12.00, 0.00, 0.00, 0.00, 1.00, 1.00, 1.00)
        #self.box2.setAntialias(AntialiasAttrib.MMultisample)
        #self.box2.setTwoSided(1)
        
        self.book = loader.loadModel('models/BookShelf')
        self.book.setPosHprScale(-12.50, 12.00, 3.24, 270.00, 0.00, 0.00, 1.26, 1.26, 1.26)
        self.book.reparentTo(render)
        
        self.desk = loader.loadModel('models/desk')
        self.desk.setPosHprScale(2.00, 16.00, 3.20, 180.00, 0.00, 0.00, 1.46, 1.46, 1.46)
        self.desk.setTag('LookAtMeFrom','S')
        self.desk.reparentTo(render)
               
        base.setBackgroundColor(0.0,0.3,0.0)
        
        self.boxes = render.attachNewNode("boxes")
        #self.boxes.setAntialias(AntialiasAttrib.MAuto)
        
        self.box4 = [None for i in range(11)]
        for i in range(5):
            self.box4[i] = loader.loadModel('models/untitled2')
            self.box4[i].reparentTo(self.boxes)
            self.box4[i].setScale(0.2)
            if (i%2) == 0: 
                self.box4[i].setPos(0, (1 * i), 9)
                self.box4[i].setTag('label', 'Samuele')
                self.box4[i].setTag('LookAtMeFrom', 'W')
            else:
                self.box4[i].setTag('label', 'Cristina')
                self.box4[i].setPos(0, (1 * i), 8.3)
                self.box4[i].setTag('LookAtMeFrom', 'E')

            self.box4[i].find("**/Cube").node().setTag('box4', str(i))
            self.box4[i].setTag('box4', str(i))
            #self.box4[i].setColor(1/(i+0.01),1/(i+0.01)*0.2,1/(i+0.01))
            
        self.box4[1].setZ(9.7)
        self.box4[0].setTag('LookAtMeFrom', 'S')
        self.box4[4].setTag('LookAtMeFrom', 'N')
        
        self.box4[2].setPosHprScale(11.00, 1.00, 5.70, 0.00, 0.00, 0.00, 0.20, 0.20, 0.20)
        
        self.box4[5] = loader.loadModel('models/untitled2')
        self.box4[5].reparentTo(self.boxes)
        self.box4[5].setScale(0.3)
        self.box4[5].setPos(80 - 2.4, 0, 2)
        self.box4[5].find("**/Cube").node().setTag('box4', '5')
        self.box4[5].setTag('box4', '5')
        self.box4[5].setTag('label', 'Cristina Fuori Schermo')
        #self.box4[5].setAntialias(AntialiasAttrib.MAuto)

        self.box4[6] = loader.loadModel('models/Book')
        #self.book3.setH(-90)
        self.box4[6].setPosHprScale(-11.50, 10.00, 4.70, 0, 0.00, 0.00, 1.25, 1.25, 1.25)
        self.box4[6].reparentTo(self.boxes)
        self.box4[6].find("**/Front").node().setIntoCollideMask(BitMask32.bit(1))
        self.box4[6].find("**/Back").node().setIntoCollideMask(BitMask32.bit(1))
        self.box4[6].find("**/Front").node().setTag('box4', '6')
        self.box4[6].find("**/Back").node().setTag('box4', '6')
        self.box4[6].setTag('box4', '6')
        self.box4[6].setTag('LookAtMeFrom', 'E')
        
        lastIndex = 6
        y = -1.67
        
        for i in range(4):
            
            lastIndex = lastIndex + 1
            y = y + 0.32

            self.box4[lastIndex] = loader.loadModel('models/Book')
            #self.book3.setH(-90)
            
            self.box4[lastIndex].setPosHprScale(y, -1.70, 4.70, -90.00, 0.00, 0.00, 1.00, 1.00, 1.00)
            self.box4[lastIndex].setColorScale(Vec4(0.5,0.5,0.5,1))
            self.box4[lastIndex].reparentTo(self.boxes)
            self.box4[lastIndex].find("**/Front").node().setIntoCollideMask(BitMask32.bit(1))
            self.box4[lastIndex].find("**/Back").node().setIntoCollideMask(BitMask32.bit(1))
            self.box4[lastIndex].find("**/Front").node().setTag('box4', str(lastIndex))
            self.box4[lastIndex].find("**/Back").node().setTag('box4', str(lastIndex))
            self.box4[lastIndex].setTag('box4', str(lastIndex))
            self.box4[lastIndex].setTag('LookAtMeFrom', 'S')
        
        self.box4[8].setH(90)
        self.box4[8].setTag('LookAtMeFrom', 'N')
        
        light5 = PointLight('pointlight3')
        plnp5 = render.attachNewNode(light5)
        plnp5.setPos(10,0, 8)
        render.setLight(plnp5)
        

#        light3 = PointLight('pointlight2')
#        plnp3 = render.attachNewNode(light3)
#        plnp3.setPos(1,1,15)
#        render.setLight(plnp3)
        

        
        self.accept("arrow_left", self.left)
        self.accept("arrow_right", self.right)
        self.accept("arrow_up", self.su)
        self.accept("arrow_down", self.giu)
        self.corrente = 0

    def LoadLight(self):
        ''' Create an Ambient light as well as a point light
        '''
        plight = AmbientLight('my plight')
        plight.setColor(VBase4(0.12, 0.12, 0.12, 1))
        plnp = render.attachNewNode(plight)
        render.setLight(plnp)

        #light2 = PointLight('pointlight')
        #plnmovingCamera = render.attachNewNode(self.followerCamera)
        #plnmovingCamera.setPos(1.00, 100.00, -8)
        #render.setLight(plnmovingCamera)
        
        light4 = PointLight('pointlight3')
        plnp4 = render.attachNewNode(light4)
        plnp4.setPos(10, 0, 8)
        #render.setLight(plnp4)
        
    
    def setLightsOn(self, model):
        
        if model == self.box_current:
            return
        
        self.ex = self.box_current
        self.box_current = model
        
        int1 = LerpColorScaleInterval(self.box_current, 0.1, Vec4(5,5,5,1))
        int2 = LerpColorScaleInterval(self.ex, 0.3, Vec4(0.5,0.5,0.5,1))
        #self.p = Parallel(int1, int2, name="Parallel Name")
        #self.p.start()
        int1.start()
        int2.start()
        
        #print self.box_current.getTag('box4')
        
        
    def cameraLookAt(self, model):
        
        if self.movingCamera != None:
            if self.movingCamera.isPlaying():
                self.movingCamera.pause()
                
        lookFrom = model.getTag("LookAtMeFrom")

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
        
        print "AttualeAt " + str(base.camera.getHpr())
        print "LookAt " + str(self.followerCamera.getHpr())
        
        if base.camera.getH() == -90 and self.followerCamera.getH() == 180:
            self.followerCamera.setH(-180)
        
        if base.camera.getH() == 180 and self.followerCamera.getH() == -90:
            self.followerCamera.setH(270)
            
        if base.camera.getH() == 270 and self.followerCamera.getH() == -90:
            self.followerCamera.setH(270)
            
        if base.camera.getH() == -180 and self.followerCamera.getH() == 90:
            self.followerCamera.setH(90)
            
        if base.camera.getH() == -90 and self.followerCamera.getH() == 90:
            self.followerCamera.setH(90)
        
        if base.camera.getH() == 180 and self.followerCamera.getH() == 0:
            self.followerCamera.setH(360)
        
        if base.camera.getH() == 0 and self.followerCamera.getH() == 180:
            self.followerCamera.setH(-180)
        
        distance = base.camera.getDistance(self.followerCamera) 
        speed = 5
        duration = distance * speed / 100
         
        if duration < 1:
            duration = 1
        
        print "Distance " + str(distance)
        print "Duration " + str(duration)
        
        self.interv1 = LerpHprInterval(base.camera, duration, self.followerCamera.getHpr(), blendType='easeInOut')
        self.interv2 = LerpPosInterval(base.camera, duration, self.followerCamera.getPos(), blendType='easeInOut')
        
        self.movingCamera = Parallel(self.interv2, self.interv1, name="Parallel Name1")
        
        self.movingCamera.start()
        
        if base.camera.getH() == 360:
            base.camera.setH(0)
        
        self.lookingAt = model
        
    def left(self):
        self.corrente = self.corrente - 1
        
        if self.corrente < 0:
            self.corrente = 10
        
        self.cameraLookAt(self.box4[self.corrente])
        self.setLightsOn(self.box4[self.corrente])
        
    def right(self):
        self.corrente = self.corrente + 1
        
        if self.corrente > 10:
            self.corrente = 0
            
        self.cameraLookAt(self.box4[self.corrente])
        self.setLightsOn(self.box4[self.corrente])
    
    def su(self):
        self.cameraLookAt(self.box4[self.corrente])
        self.setLightsOn(self.box4[self.corrente])
        
    def giu(self):
        self.cameraLookAt(self.box3)
        self.setLightsOn(self.box4[self.corrente])
        
    def cameraGoHome(self):
        print "Camera go home!"
        
        if self.movingCamera != None:
            if self.movingCamera.isPlaying():
                self.movingCamera.pause()
            
        self.followerCamera.setPos(self.cameraOriginalPos)
        self.followerCamera.setHpr(self.cameraOriginalHpr)
        
        self.interv = LerpHprInterval(base.camera, 1 , self.followerCamera.getHpr(), blendType='easeInOut')
        self.interv2 = LerpPosInterval(base.camera, 1 , self.followerCamera.getPos(), blendType='easeInOut')
        
        self.movingCamera = Parallel(self.interv2, self.interv, name="Parallel Name2")
        self.movingCamera.start()

    def LoadCamera(self):
        self.followerCamera = render.attachNewNode("follower")

        # Camera
        self.cameraOriginalPos = Vec3(0.00, -17.00, 8.00)
        self.cameraOriginalHpr = Vec3(0,0,0) 
        
        self.cameraGoHome()
        
        #mat=Mat4(camera.getMat())
        #mat.invertInPlace()
        #base.mouseInterfaceNode.setMat(mat)

# Application code
if __name__ == "__main__":

    samuele = World()
    run()
