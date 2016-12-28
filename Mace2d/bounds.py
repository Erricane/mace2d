import numpy as np
from vector import *
import unittest

class Bounds:
    #TODO error check, dimesnions must be positive

    def __init__(self, origin, dimension):
        self.origin = origin.copy()
        self.dimension = dimension.copy()
        self.reformat()
        
        
    def __eq__(self,other):
        return (
            self.origin == other.origin and self.dimension == other.dimension
        )
        
    def __repr__(self):
        return (
            "Bounds<" +
            str(self.origin) + "," +
            str(self.dimension) + ">" 
        )
            
    def reformat(self):
        self.origin.x = min(self.origin.x, self.origin.x + self.dimension.x)
        self.origin.y = min(self.origin.y, self.origin.y + self.dimension.y)
        self.dimension.x = abs(self.dimension.x)
        self.dimension.y = abs(self.dimension.y)
        
    def copy(self):
        return Bounds(self.origin,self.dimension)

        
    def sweep(self, vector):
        return Bounds(
            self.origin + Vector(min(vector.x, 0),min(vector.y, 0)),
            self.dimension + Vector(abs(vector.x),abs(vector.y))
        )
        
    def pad(self,width,height):
        self.origin -= Vector(width,height)
        self.dimension += 2 * Vector(width,height)
    
    def width(self):
        return self.dimension.x
        
    def height(self):
        return self.dimension.y
        
    def left(self):
        return self.origin.x
        
    def right(self):
        return self.left() + self.width()

    def top(self):
        return self.origin.y
        
    def bottom(self):
        return self.top() + self.height()
        
    def intersects(self,other):
        return(
            self.top() <= other.bottom() and
            self.bottom() >= other.top() and
            self.left() <= other.right() and
            self.right() >= other.left()
        )

class Bounds_Test(unittest.TestCase):
    
    def test_negative_initiation(self):
        bounds = Bounds(Vector(3,4),Vector(-6,-8))
        self.assertEqual(bounds.left(),-3)
        self.assertEqual(bounds.top(),-4)
        self.assertEqual(bounds.width(),6)
        self.assertEqual(bounds.height(),8)
        bounds = Bounds(Vector(-3,-4),Vector(-6,-8))
        self.assertEqual(bounds.left(),-9)
        self.assertEqual(bounds.top(),-12)
        self.assertEqual(bounds.width(),6)
        self.assertEqual(bounds.height(),8)
        bounds = Bounds(Vector(-3, -4),Vector(6, 8))
        self.assertEqual(bounds.left(),-3)
        self.assertEqual(bounds.top(),-4)
        self.assertEqual(bounds.width(),6)
        self.assertEqual(bounds.height(),8)

        
    def test_sweep(self):
        bounds = Bounds(Vector(0, 0),Vector(20, 20))
        bounds = bounds.sweep(Vector(42, 35))
        self.assertEqual(bounds.left(),0)
        self.assertEqual(bounds.top(),0)
        self.assertEqual(bounds.width(),62)
        self.assertEqual(bounds.height(),55)
        bounds = Bounds(Vector(0, 0),Vector(20,20))
        bounds = bounds.sweep(Vector(-10, -10))
        self.assertEqual(bounds.left(),-10)
        self.assertEqual(bounds.top(),-10)
        self.assertEqual(bounds.width(),30)
        self.assertEqual(bounds.height(),30)
        self.assertEqual(bounds.right(),20)
        self.assertEqual(bounds.bottom(),20)
        bounds = Bounds(Vector(10, 10),Vector(-20,-20))
        bounds = bounds.sweep(Vector(-3,-4))
        self.assertEqual(Bounds(Vector(-13,-14),Vector(23,24)),bounds)
        
    def test_pad_copy(self):
        b0 = Bounds(Vector(0, 0),Vector(20, 20))
        b1 = b0.copy()
        b2 = b0 #reference
        b4 = Bounds(Vector(50, 50),Vector(20, 20))
        b5 = b4.copy()
        b6 = b5.copy()
        b0.pad(10,10)
        b4.pad(20,0)
        b5.pad(0,20)
        b6.pad(0,0)
        self.assertEqual(Bounds(Vector(-10,-10),Vector(40,40)),b0)
        self.assertEqual(Bounds(Vector(0,0),Vector(20,20)),b1)
        self.assertEqual(Bounds(Vector(-10,-10),Vector(40,40)),b2)
        self.assertEqual(Bounds(Vector(30,50),Vector(60,20)),b4)
        self.assertEqual(Bounds(Vector(50,30),Vector(20,60)),b5)
        self.assertEqual(Bounds(Vector(50, 50),Vector(20, 20)),b6)
        
        
    def intersect(self):
        b0 = Bounds(Vector(-10, -10),Vector(20, 20))
        b1 = Bounds(Vector(-25, -25),Vector(20, 20))
        b2 = Bounds(Vector(5, 5),Vector(20, 20))
        b3 = Bounds(Vector(10,10),Vector(1,1))
        
        self.assertTrue(b0.intersects(b1))
        self.assertFalse(b1.intersects(b2))
        self.assertTrue(b0.intersects(b2))
        self.assertTrue(b0.intersects(b3))
        
        
if __name__ == "__main__":
    unittest.main()
    