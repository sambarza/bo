from direct.fsm.FSM import FSM, RequestDenied

from world.Events import Events

class ywnThingFsm(FSM):

    NOTHING = 'NOTHING'
    
    def __init__(self, linkedThing):

        self.AtHome = 'AtHome'
        self.AtHomeWithLightsOn = 'AtHomeWithLightsOn'
        self.AtHomeFocusRequested = 'AtHomeFocusRequested'
        self.AtHomeWithFocus = 'AtHomeWithFocus'
        self.AtDeskWithFocus = 'AtDeskWithFocus'
        self.AtDesk = 'AtDesk'
        
        FSM.__init__(self, 'ywnlinkedThingFsm')
        
        self.linkedThing = linkedThing
        
        self.state = self.AtHome
                
        self.nextState = {
                          
            (self.AtHome, Events.mouseOnYou) : self.AtHomeWithLightsOn,
            (self.AtHome, Events.leftMouseClick) : self.AtHomeWithFocus,
            (self.AtHome, Events.rightMouseClick) : self.AtHome,
            (self.AtHome, Events.mouseOnOthers) : self.AtHome,
            
            (self.AtHomeWithLightsOn, Events.leftMouseClick) : self.AtHomeFocusRequested,
            (self.AtHomeWithLightsOn, Events.mouseOnOthers) : self.AtHome,
            (self.AtHomeWithLightsOn, Events.rightMouseClick) : self.AtHomeWithLightsOn,
            
            (self.AtHomeFocusRequested, Events.leftMouseClick) : self.NOTHING,
            (self.AtHomeFocusRequested, Events.rightMouseClick) : self.NOTHING,
            (self.AtHomeFocusRequested, Events.mouseOnOthers) : self.NOTHING,
            (self.AtHomeFocusRequested, Events.mouseOnYou) : self.NOTHING,
            (self.AtHomeFocusRequested, Events.cameraArrivedToYou) : self.AtHomeWithFocus,
            (self.AtHomeFocusRequested, Events.cameraDeviated) : self.AtHome,
            
            (self.AtHomeWithFocus, Events.leftMouseClick) : self.AtDeskWithFocus,
            (self.AtHomeWithFocus, Events.rightMouseClick) : self.AtHome,
            (self.AtHomeWithFocus, Events.mouseOnYou) : self.NOTHING,
            (self.AtHomeWithFocus, Events.mouseOnOthers) : self.NOTHING,
            (self.AtHomeWithFocus, Events.cameraGoingHome) : self.AtHome,
            (self.AtHomeWithFocus, Events.focusRequestedByOthers) : self.AtHome,
            
            (self.AtDeskWithFocus, Events.mouseOnYou) : self.NOTHING,
            (self.AtDeskWithFocus, Events.mouseOnOthers) : self.NOTHING,
            (self.AtDeskWithFocus, Events.leftMouseClick) : self.NOTHING,
            (self.AtDeskWithFocus, Events.rightMouseClick) : self.AtDesk
            
        }

    def defaultFilter(self, request, args):
        
        key = (self.state, request)
        foundNextState = self.nextState.get(key)
 
        if foundNextState == None:
            raise RequestDenied, "Thing %s id %s %s (from state: %s)" % (self.linkedThing.thingName, self.linkedThing.Id, request, self.state)
            
        if foundNextState == self.NOTHING:
            return None

        return foundNextState
       
    def enterAtHome(self):
        
        print self.linkedThing.getThingInfo() + " enterAtHome"
       
        self.linkedThing.lightsOff()
            
    def exitAtHome(self):
        
        print self.linkedThing.getThingInfo() + " exitAtHome"
        
    def enterAtHomeFocusRequested(self):
        
        print self.linkedThing.getThingInfo() +  " enterAtHomeFocusRequested"
        
        self.linkedThing.requestFocus()
   
    def exitAtHomeFocusRequested(self):
        
        print self.linkedThing.getThingInfo() +  " exitAtHomeFocusRequested"
        
    def enterAtHomeWithFocus(self):
        
        print self.linkedThing.getThingInfo() +  " enterAtHomeWithFocus"
        
        self.linkedThing.gotFocus()
        
    def exitAtHomeWithFocus(self):
        
        print self.linkedThing.getThingInfo() +  " exitAtHomeWithFocus"
        
    def enterAtHomeWithLightsOn(self):
        
        print self.linkedThing.getThingInfo() + " enterAtHomeWithLightsOn"
        
        self.linkedThing.lightsOn()
        
    def exitAtHomeWithLightsOn(self):
        
        print self.linkedThing.getThingInfo() + " exitAtHomeWithLightsOn"
