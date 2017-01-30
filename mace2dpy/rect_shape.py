from vector import *

class Rect_Shape:
    def __init__(
        self,
        position = Vector(0,0),
        orientation = Vector(1,0),
        inverse_orientation = Vector(1,0),
        offset = Vector(0,0),
        width = 10,
        height = 10
    ):
        self.position = position
        self.orientation = None
        self.inverse_orientation = None
        self.offset = offset
        self.width = width
        self.height = height

        
        
    def get_support(self, beam):
        
        #
        
        #return support based on the direaction of beam