import numpy as np
import unittest

class Bounds:
    #error check, dimesnions must be positive
    
    
    def __init__(self, origin, dimension):
        #Bounds have their own vectors and will always copy
        self.origin = np.array([0,0])
        self.dimension = np.array([0,0])
        self.origin[0] = min(origin[0], origin[0] + dimension[0])
        self.origin[1] = min(origin[1], origin[1] + dimension[1])
        self.dimension[0] = abs(dimension[0])
        self.dimension[1] = abs(dimension[1])
        
    def reinitialize(self, origin, dimension):
        self.origin[0] = min(origin[0], origin[0] + dimension[0])
        self.origin[1] = min(origin[1], origin[1] + dimension[1])
        self.dimension[0] = abs(dimension[0])
        self.dimension[1] = abs(dimension[1])
        return self
        
    def set_origin(self, origin):
        self.origin[0] = origin[0]
        self.origin[1] = origin[1]
        return self
        
    def offset(self, position):
        self.origin[0] += position[0]
        self.origin[1] += position[1]
        return self
        
    def sweep(self, vector):
        self.origin[0] = self.origin[0] + min(vector[0], 0)
        self.origin[1] = self.origin[1] + min(vector[1], 0)
        self.dimension[0] += abs(vector[0])
        self.dimension[1] += abs(vector[1])
        return self
        

    def set_dimension(self, dimension):
        if dimension[0] < 0 or dimension[1] < 0:
            raise ValueError(
                "Coordinates for setting a bounds' dimension must be positive"
            )
        self.dimension[0] = dimension[0]
        self.dimension[1] = dimension[1]
        return self
        
    def get_origin(self):
        return self.origin
        
    def get_width(self):
        return float(self.dimension[0])
        
    def get_height(self):
        return float(self.dimension[1])
        
    def get_left(self):
        return float(self.origin[0])
        
    def get_right(self):
        return self.get_left() + self.get_width()

    def get_top(self):
        return float(self.origin[1])
        
    def get_bottom(self):
        return self.get_top() + self.get_height()
        
    def intersects(self,other):
        return(
            self.get_top() < other.get_bottom() and
            self.get_bottom() > other.get_top() and
            self.get_left() < other.get_right() and
            self.get_right() > other.get_left()
        )

class Bounds_Test(unittest.TestCase):
    
    def test_negative_initiation(self):
        bounds = Bounds(np.array([3,4]),np.array([-6,-8]))
        self.assertEqual(bounds.get_left(),-3)
        self.assertEqual(bounds.get_top(),-4)
        self.assertEqual(bounds.get_width(),6)
        self.assertEqual(bounds.get_height(),8)
        bounds = Bounds(np.array([-3,-4]),np.array([-6,-8]))
        self.assertEqual(bounds.get_left(),-9)
        self.assertEqual(bounds.get_top(),-12)
        self.assertEqual(bounds.get_width(),6)
        self.assertEqual(bounds.get_height(),8)
        bounds = Bounds(np.array([-3, -4]),np.array([6, 8]))
        self.assertEqual(bounds.get_left(),-3)
        self.assertEqual(bounds.get_top(),-4)
        self.assertEqual(bounds.get_width(),6)
        self.assertEqual(bounds.get_height(),8)
        bounds.reinitialize(np.array([3,4]),np.array([-6,-8]))
        self.assertEqual(bounds.get_left(),-3)
        self.assertEqual(bounds.get_top(),-4)
        self.assertEqual(bounds.get_width(),6)
        self.assertEqual(bounds.get_height(),8)
        bounds.reinitialize(np.array([-3,-4]),np.array([-6,-8]))
        self.assertEqual(bounds.get_left(),-9)
        self.assertEqual(bounds.get_top(),-12)
        self.assertEqual(bounds.get_width(),6)
        self.assertEqual(bounds.get_height(),8)
        bounds.reinitialize(np.array([-3, -4]),np.array([6,8 ]))
        self.assertEqual(bounds.get_left(),-3)
        self.assertEqual(bounds.get_top(),-4)
        self.assertEqual(bounds.get_width(),6)
        self.assertEqual(bounds.get_height(),8)
    
    def test_offset(self):
        bounds = Bounds(np.array([0, 0]),np.array([20, 20]))
        bounds = bounds.offset(np.array([4, 5]))
        self.assertEqual(bounds.get_left(),4)
        self.assertEqual(bounds.get_top(),5)
        
    def test_sweep(self):
        bounds = Bounds(np.array([0, 0]),np.array([20, 20]))
        bounds = bounds.sweep(np.array([42, 35]))
        self.assertEqual(bounds.get_left(),0)
        self.assertEqual(bounds.get_top(),0)
        self.assertEqual(bounds.get_width(),62)
        self.assertEqual(bounds.get_height(),55)
        bounds = Bounds(np.array([0, 0]),np.array([20, 20]))
        bounds = bounds.sweep(np.array([-10, -10]))
        self.assertEqual(bounds.get_left(),-10)
        self.assertEqual(bounds.get_top(),-10)
        self.assertEqual(bounds.get_width(),30)
        self.assertEqual(bounds.get_height(),30)
        self.assertEqual(bounds.get_right(),20)
        self.assertEqual(bounds.get_bottom(),20)
if __name__ == "__main__":
    bounds_test_suite = unittest.TestLoader().loadTestsFromTestCase(Bounds_Test)
    