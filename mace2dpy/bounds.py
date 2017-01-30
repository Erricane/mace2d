from vector import *
import unittest

class Bounds:
    #TODO error check, dimesnions must be positive

    def __init__(self, origin, dimension):
        #initialize with vectors, tuples and list
        self.origin = Vector(origin[0], origin[1])
        self.dimension = Vector(dimension[0], dimension[1])
        
        #make bounds so that dimension is always positive
        self.reformat()
        
    
    #for testing only, bounds can be compared    
    def __eq__(self,other):
        return (
            self.origin == other.origin and self.dimension == other.dimension
        )
    def __ne__(self,other):
        return not self == other
        
        
    def __repr__(self):
        return (
            "Bounds(" +
            str(self.origin)[6:]  + ", " +  #[6:] removes "vector"
            str(self.dimension)[6:] + ")" 
        )
        
    #make bounds so that dimension is always positive
    def reformat(self):
        self.origin.x = min(self.origin.x, self.origin.x + self.dimension.x)
        self.origin.y = min(self.origin.y, self.origin.y + self.dimension.y)
        self.dimension.x = abs(self.dimension.x)
        self.dimension.y = abs(self.dimension.y)
        return self
        
    def copy(self):
        return Bounds(+self.origin, +self.dimension)

    def __pos__(self):
        return self.copy()
        
    def sweep(self, vector):
        return Bounds(
            self.origin + Vector(min(vector[0], 0),min(vector[1], 0)),
            self.dimension + Vector(abs(vector[0]),abs(vector[1]))
        )
        
    def pad(self, padding):
        if padding < 0:
            raise ValueError("padding must not be negative")
        return Bounds(
            self.origin - Vector(padding, padding),
            self.dimension + 2 * Vector(padding, padding)
        )
    
    def offset(self, vector):
        self.origin += vector
    
    def width(self):
        return self.dimension.x
        
    def height(self):
        return self.dimension.y
        
    def left(self):
        return self.origin.x
        
    def right(self):
        return self.left() + self.width()

    def bottom(self):
        return self.origin.y
        
    def top(self):
        return self.bottom() + self.height()
        
    def offset(self, vector):
        return Bounds(
            self.origin + vector,
            self.dimension
        )
        
    def intersects(self,other):
        return(
            self.top() >= other.bottom() and
            self.bottom() <= other.top() and
            self.left() <= other.right() and
            self.right() >= other.left()
        )
        

class Bounds_Test(unittest.TestCase):
    
    def test_copy_pos(self):
        global b0, b00, b01, b02, b03, b1, b2, b3, b4, b5
        self.reset()
        
        #similarity equality
        self.assertEqual(b0, b0)
        self.assertEqual(b0, b00)
        self.assertEqual(b00, b01)
        self.assertEqual(b01, b02)
        self.assertEqual(b02, b03)
        
        c0 = b0             #reference
        c1 = b0.copy()      #copy
        c2 = +b0            #copy
        b0.origin = Vector(0,0)
        
        self.assertEqual(c0,b0)
        self.assertEqual(c1,c2)
        self.assertEqual(c0, Bounds((0,0),(2.6,2.5)))
        self.assertEqual(c1, Bounds((-1.2,-1.25),(2.6,2.5)))
        self.assertNotEqual(c0,c1)
        
    def test_sweep(self):
        global b0, b00, b01, b02, b03, b1, b2, b3, b4, b5
        self.reset()
        
        #no sweep
        self.assertEqual(b0.sweep((0,0)), Bounds((-1.2,-1.25),(2.6,2.5)))
        
        
        self.assertEqual(b1.sweep((1.3,0)), Bounds((1.0,1.0),(2.3,1.0)))
        self.assertEqual(b2.sweep((6.6,0.8)), Bounds((-2.0,-2.0),(7.6,1.8)))
        self.assertEqual(b3.sweep((-0.3,-0.6)), Bounds((-2.8,-3.1),(1.3,1.6)))
        self.assertEqual(b4.sweep((21.0,-3)), Bounds((100.0,97.0),(41.0,23.0)))
        self.assertEqual(b5.sweep((-21.0,3)), Bounds((84.0,105.0),(31.0,13.0)))
        
        
    def test_pad(self):
        global b0, b00, b01, b02, b03, b1, b2, b3, b4, b5
        self.reset()
        
        #no padding
        self.assertEqual(b0.pad(0), Bounds((-1.2,-1.25),Vector(2.6,2.5)))
        
        
        self.assertEqual(b1.pad(2.6), Bounds((-1.6,-1.6),(6.2,6.2)))
        self.assertEqual(b2.pad(6.7), Bounds((-8.7,-8.7),(14.4,14.4)))
        self.assertEqual(b3.pad(0.4), Bounds((-2.9,-2.9),(1.8,1.8)))
        self.assertEqual(b4.pad(0.9), Bounds((99.1,99.1),(21.8,21.8)))
        self.assertEqual(b5.pad(2), Bounds((103.0,103.0),(14.0,14.0)))
        
    def test_intersect(self):
        global b0, b00, b01, b02, b03, b1, b2, b3, b4, b5
        self.reset()
        
        #self intersect
        self.assertTrue(b00.intersects(b00))
        
        #similar intersect
        self.assertTrue(b01.intersects(b02))
        
        # test b0 - b3
        self.assertTrue(b1.intersects(b0))
        self.assertTrue(b2.intersects(b0))
        self.assertTrue(b2.intersects(b3))
        self.assertFalse(b2.intersects(b1))
        self.assertFalse(b3.intersects(b0))
        
        #test b0, b4, b5
        self.assertTrue(b4.intersects(b5))
        self.assertTrue(b5.intersects(b4)) #communative
        self.assertFalse(b4.intersects(b0))
        
        
    def reset(self):
        global b0, b00, b01, b02, b03, b1, b2, b3, b4, b5
        
        #b0x are all equivalent,
        b00 = Bounds((-1.2,-1.25),Vector(2.6,2.5))
        b01 = Bounds((1.4,1.25),(-2.6,-2.5))
        b02 = Bounds(Vector(1.4,-1.25),(-2.6,2.5))
        b03 = Bounds(Vector(-1.2,1.25),Vector(2.6,-2.5))
        b0 = +b00
        
        #intersect b0x, not each other
        b1 = Bounds((1,1),(1,1))
        b2 = Bounds((-1,-1),(-1,-1))
        
        #intersects b2 but not b0x
        b3 = Bounds((-1.5,-1.5),(-1,-1))
        
        #does not intersect b0 - b3, b4  contains b5 
        b4 = Bounds((100,100),(20,20))
        b5 = Bounds((105,105),(10,10))
        
        
if __name__ == "__main__":
    print("bounds.py")
    unittest.main()
    