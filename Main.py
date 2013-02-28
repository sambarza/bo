'''
Created on 10/feb/2013

@author: sambarza@gmail.com
'''

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject

from pandac.PandaModules import AmbientLight
from pandac.PandaModules import PointLight
from pandac.PandaModules import VBase4

from world.MouseWatcher import MouseWatcher
from world.Camera import Camera
from world.Things import Things
from world.Picker import Picker
from world.Tooltip import Tooltip
from world.EventHandler import EventHandler

from world.things.book.Book import Book
from world.things.bookshelf.Bookshelf import Bookshelf
from world.things.box.Box import Box
from world.things.lightswitch.Lightswitch import Lightswitch
from world.things.calculator.Calculator import Calculator

#from panda3d.core import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

class Ywn(ShowBase):
 
    def __init__(self):
        
        ShowBase.__init__(self)
 
        self.initialize()
        
        self.camera.goHome()
        
    def initialize(self):
        
        self.disableMouse()
        self.initializeEventHandler()
        self.initializeCamera()
        self.initializeThings()
        self.initializePickerRay()
        self.initializeMouseWatcher()
        self.initializeTooltip()
        self.loadHouse()
        self.loadLights()
        self.loadThings()
        
    def initializeCamera(self):
        
        self.camera = Camera(self.render, self.camera, self.eventHandler)
        
        self.camLens.setFov(90)
               
    def initializeThings(self):
        
        self.focusOn = None
        
        self.things = Things(self.render)
        
    def initializePickerRay(self):
        
        self.picker = Picker(self.camera.camera, self.mouseWatcherNode, self.camNode, self.things)

    def initializeMouseWatcher(self):
    
        self.mouseWatcher = MouseWatcher(self, self.taskMgr, self.eventHandler, self.picker)
        
    def initializeTooltip(self):
        
        self.tooltip = Tooltip(self)
        
    def initializeEventHandler(self):
        
        self.eventHandler = EventHandler(self)
        
    def loadHouse(self):
        
        self.house = loader.loadModel('models/bedroom')
        self.house.reparentTo(render)
        self.house.setPosHprScale(0.00, 0.00, 0.00, 180.00, 0.00, 0.00, 1.26, 1.26, 1.26)
        
        #self.house = loader.loadModel('models/FarmHouse/FarmHouse.egg')
        #self.house.reparentTo(render)
        #self.house.setPosHprScale(-6.47, 17.49, 1.80, 180.00, 0.00, 0.00, 5.00, 5.00, 5.00)
        
    def loadLights(self):

        plight = AmbientLight('my plight')
        plight.setColor(VBase4(0.12, 0.12, 0.12, 1))
        self.plnp = self.render.attachNewNode(plight)
        self.render.setLight(self.plnp)

        light4 = PointLight('pointlight3')
        plnp4 = self.render.attachNewNode(light4)
        plnp4.setPos(10, 0, 8)
    
        light5 = PointLight('pointlight5')
        self.plnp5 = self.render.attachNewNode(light5)
        self.plnp5.setPos(10,0, 8)
        self.render.setLight(self.plnp5)
        
    def loadThings(self):
        
        Book1 = Book(self)
        Book1.setPosHprScale(-11.50, 10.00, 4.70, 0, 0.00, 0.00, 1.25, 1.25, 1.25)
        Book1.setLookFrom('E')
        Book1.lightsOff()
        
        self.things.add(Book1)
        
        Book2 = Book(self)
        Book2.setPosHprScale(-11.50, 11.00, 4.70, 0, 0.00, 0.00, 1.25, 1.25, 1.25)
        Book2.setLookFrom('E')
        Book2.lightsOff()
        
        self.things.add(Book2)
        
        Book2 = Book(self)
        Book2.setPosHprScale(-11.50, 12.00, 4.70, 0, 0.00, 0.00, 1.25, 1.25, 1.25)
        Book2.setLookFrom('E')
        Book2.lightsOff()
        
        self.things.add(Book2)
        
        Book2 = Book(self)
        Book2.setPosHprScale(-11.50, 13.00, 4.70, 0, 0.00, 0.00, 1.25, 1.25, 1.25)
        Book2.setLookFrom('E')
        Book2.lightsOff()
        
        self.things.add(Book2)
        
        Book2 = Book(self)
        Book2.setPosHprScale(-11.50, 13.00, 6.50, 0, 0.00, 0.00, 1.25, 1.25, 1.25)
        Book2.setLookFrom('E')
        Book2.lightsOff()
        
        self.things.add(Book2)
        
        bookshelf = Bookshelf(self)
        bookshelf.setPosHprScale(-12.50, 12.00, 3.24, 270.00, 0.00, 0.00, 1.26, 1.26, 1.26)
        bookshelf.setLookFrom('E')
        
        self.things.add(bookshelf)
        
        box = Box(self)
        box.setPosHprScale(11.00, 1.00, 5.70, 0.00, 0.00, 0.00, 0.20, 0.20, 0.20)
        box.setLookFrom('W')
        
        self.things.add(box)
        
        lightswitch = Lightswitch(self)
        lightswitch.setPosHprScale(11.50, 3.5, 7.0, 90.00, 0.00, 0.00, 5, 5, 5)
        lightswitch.setLookFrom('W')
        
        self.things.add(lightswitch)
        
        calculator = Calculator(self)
        calculator.setPosHprScale(11.50, 5, 7.0, 90.00, -90.00, 0.00, 1, 1, 1)
        calculator.setLookFrom('W')
        
        self.things.add(calculator)
        
    def setFocusOn(self, thing):
        
        self.focusOn = thing
        
# Start
ywn = Ywn()
ywn.run()
