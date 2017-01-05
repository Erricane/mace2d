from vector import *
from gjk import *

class Test_Shape:
    
    def __init__(self,position):
        self.position = Vector(position[0], position[1])
        
    def get_support(self, beam):
        return self.position
        
class Test_Shape2:
    def __init__(self,position,width,height):
        self.position = Vector(position[0], position[1])
        self.width = width
        self.height = height
        
    def get_support(self,beam):
        
        #Beam to the Right
        if beam.x > 0:
            if beam.y > 0:   #beam to the top-right
                return self.position + Vector(self.width,self.height) / 2
            else:            #beam to the bottom-right
                return self.position + Vector(self.width,-self.height) / 2
          
        #beam to the Left
        else:

            if beam.y > 0:   #beam to the top-left
                return self.position + Vector(-self.width,self.height) / 2
            else:            #beam to the bottom-left
                return self.position + Vector(-self.width,-self.height) / 2