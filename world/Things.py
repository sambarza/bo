'''
Created on 11/feb/2013

@author: sambarza@gmail.com
'''

class Things(object):
    '''
    classdocs
    '''


    def __init__(self, render):
        '''
        Constructor
        '''
        self.things = dict()
        self.node = render.attachNewNode("things")
    
    def add(self, thing):
        
        self.things[thing.Id] = thing
        thing.reparentTo(self.node)
        
    def getById(self, thing_id):
        
        return self.things[thing_id]