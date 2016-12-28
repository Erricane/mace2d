"""
Shape:
top()
left()
right()
bottom()

to_shape_position(position)
"""
import numpy as np
from bounds import *


class Point: #Containable

    def __init__(self, offset):
        self.offset = offset
    
    def get_offset(self):
        return self.offset
        
    def get_bounds(self):
        return Bounds(
            self.offset,
            np.array([0, 0])
        )
        
        

        
class Rectangle:
    
    
    def __init__(self, left, top, right, bottom):
        #TODO, make this safe to negatives
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.offset = np.array([0,0])
        
    def get_offset(self):
        return self.offset
        
        
    def get_bounds(self):
        return Bounds(
            np.array([-self.left, -self.top]),
            np.array([self.right + self.left, self.bottom + self.top])
        )

