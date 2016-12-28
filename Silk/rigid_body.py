import numpy as np

class Rigid_Body:
    def __init__(self,position,orientation = np.array([0,0])):
        self.position = position
        self.orientation = orientation
        
    def get_position(self):
        return self.position
        
    def get_orientation(self):
        return self.orientation
        
        