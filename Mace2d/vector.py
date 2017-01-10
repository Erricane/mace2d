from about_equal import * 

class Vector:
    
    def __init__(self,x = 0., y = 0.):
        self.x = float(x)
        self.y = float(y)
            
    def copy(self):
        return Vector(self.x, self.y)
        
    def norm(self):
        return  self.sqr_norm() ** 0.5
        
    def sqr_norm(self):
        return self.x * self.x + self.y * self.y
        
    # to string    
    def __repr__(self):
        return (
            "Vector(" +
            str(self.x) + ", " +
            str(self.y) + ")"
        )
            
    # equals (A == B)
    def __eq__(self,other):
        try:
            return (
                about_equal(self.x,other[0]) and 
                about_equal(self.y,other[1])
            )
        except TypeError:
            return False
            

        
    # equals (A != B)
    def __ne__(self,other):
        return not self == other
        
    # add (A + B)
    def __add__(self,other):
        return Vector(
            self.x + other[0],
            self.y + other[1]
        )
        
    # subtract (A - B)
    def __sub__(self,other):
        return Vector(
            self.x - other[0],
            self.y - other[1]
        )
        
    # orient by vector ( (A) .star (B) )
    def star (self, other):
        return Vector(
            self.x * other[0] - self.y * other[1],
            self.x * other[1] + self.y * other[0]
        )
    
    # cross product ( (A) .cross (B) )
    def cross (self,other):
        return self.x * other[1] - self.y * other[0]
    
    # dot  ( (A) .dot (B) )
    def dot (self,other):
        return self.x * other[0] + self.y * other[1]
     
    # scalar multiply (A * b) or (b * A)
    def __mul__(self,scalar):
        try:
            return Vector(
                self.x * float(scalar),
                self.y * float(scalar)
            )   
        except AttributeError:
            raise TypeError(
                "unsupported operand type(s) for *: 'Vector' and 'Vector'"
            )
    def __rmul__(self,scalar):
        return self * float(scalar)
        
    # scalar divide (A / b)
    def __truediv__(self,scalar):
        try:
            return Vector(
                self.x / float(scalar),
                self.y / float(scalar)
            )
        except AttributeError:
            raise TypeError(
                "unsupported operand type(s) for /: 'Vector' and 'Vector'"
            )
    def __div__(self,scalar):
        try:
            return Vector(
                self.x / float(scalar),
                self.y / float(scalar)
            )
        except AttributeError:
            raise TypeError(
                "unsupported operand type(s) for /: 'Vector' and 'Vector'"
            )
      
    # absolute ( abs(A) )
    def __abs__(self):
        return Vector(abs(self.x), abs(self.y))

    # negate (-A)
    def __neg__(self):
        return Vector(-self.x, -self.y)
        
    # invert (~A)
    def __invert__(self):
        return Vector(self.x, - self.y)
        
    # positive (+A) 
    # also used to copy (aka. dereferencing)
    def __pos__(self):
        return Vector(self.x, self.y)
        
        
    #A[0] is A.x and A[1] is A.y
    def __getitem__(self,key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else: 
            raise IndexError("Vector index out of range")
            
    # perp vector on the left side of A
    def left_perp(self):
        return Vector(-self.y, self.x)
        
    # perp vector on the right side of A
    def right_perp(self):
        return Vector(self.y, -self.x)
        
    def leftof(self,other):
        return along(self, left_perp(other))
    
    def rightof(self,other):
        return along(self, right_perp(other))
    
    def alongness(self,other):
        if other != Vector(0,0)
        return dot(self,other) / sqr_norm(other) 
    
    def againstness(self,other):
        return -alongness(self,other)
    
    def along(self,other):
        return dot(self,other) > 0
    
    def against(self,other):
        return dot(self,other) < 0 
        
    #projection
    def project(self,other):
        return other * alongness(self,other)
        
    #Alongness and Againstness are projection properties
    
    
def left_perp(vector):
    return vector.left_perp()
    
def right_perp(vector):
    return vector.right_perp()
    
def leftof(vector1,vector2):
    return vector1.leftof(vector2)
    
def rightof(vector1,vector2):
    return vector1.rightof(vector2)
    
def norm(vector):
    return vector.norm()

def sqr_norm(vector):
    return vector.sqr_norm()
    
def dot(vector1,vector2):
    return vector1.dot(vector2)
    
def cross(vector1,vector2):
    return vector1.cross(vector2)
    
def star(vector1,vector2):
    return vector1.star(vector2)
    
def project(vector1, vector2):
    return vector1.project(vector2)
    
def along(vector1, vector2):
    return vector1.along(vector2)

def alongness(vector1,vector2):
    return vector1.alongness(vector2)

def against(vector1,vector2):
    return vector1.against(vector2)

def againstness(vector1,vector2):
    return vector1.againstness(vector2)
    
def abs_equal(vector1,vector2):
    return vector1.x == vector2.x and vector1.y == vector2.y
    
def decrease(vector, value):
    if value*value > sqr_norm(vector) :
        return Vector(0,0)
    vector_norm = norm(vector)
    return (vector_norm - value) / vector_norm * vector
    
    


import unittest      

class Vector_Test(unittest.TestCase):
    
    
    def test_copy_pos(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
        
        u0 = v0.copy()
        u1 = v4.copy()
        u2 =+ v8            #+A is equivanormt to A.copy()
        
        u3 = Vector(1,1)
        u4 = Vector(-1,-1)
        u5 = Vector(0,0)
        u6 = Vector(0,0)
        
        
        u4 = u3.copy()      #copy
        u5 = u3             #reference 
        u6 =+ u3            #copy
        u3.x = 100.0
        
        self.assertEqual(u0, Vector(0,0))
        self.assertEqual(u1, (0,-1))            #tuple test
        self.assertEqual(u2, Vector(0.8,-0.3))
        self.assertEqual(u3, Vector(100,1))
        self.assertEqual(u4, Vector(1,1))
        self.assertEqual(u5, Vector(100,1))
        self.assertEqual(u6, Vector(1,1))
        
        
    def test_norm_sqr_norm(self):
        #implicitly as tests A.sqr_norm()
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
        
        self.assertEqual(v0.norm(), 0)
        self.assertEqual(v1.norm(), 1)
        self.assertEqual(v2.norm(), 1)
        self.assertEqual(v3.norm(), 1)
        self.assertEqual(v4.norm(), 1)
        self.assertEqual(v5.norm(), 6.4031242374328485)
        self.assertEqual(v6.norm(), 6.324555320336759)
        self.assertEqual(v7.norm(), 9.9)
        self.assertEqual(v8.norm(), 0.8544003745317532)

    
    def test_eq(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
        
        #self equal
        self.assertTrue(v0 == v0)
        self.assertTrue(v1 == v1)
        self.assertTrue(v2 == v2)
        self.assertTrue(v3 == v3)
        #other equal
        self.assertTrue(v4 == Vector(0,-1))
        self.assertTrue(v5 == (5,4))  #tuple test
        self.assertTrue(v6 == Vector(6,-2))
        self.assertTrue(v7 == Vector(-9.9,0))
        self.assertTrue(v8 == Vector(0.8,-0.3))
        #not equal
        self.assertFalse(v0 == v1)
        self.assertFalse(v2 == v3)
        self.assertFalse(v4 == v5)
        self.assertFalse(v6 == v7)
    
    def test_ne(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
    
        #self equal
        self.assertFalse(v0 != v0)
        self.assertFalse(v1 != v1)
        self.assertFalse(v2 != v2)
        self.assertFalse(v3 != v3)
        #other equal
        self.assertFalse(v4 != (0,-1))              #tuple test
        self.assertFalse(v5 != Vector(5,4))
        self.assertFalse(v6 != Vector(6,-2))
        self.assertFalse(v7 != Vector(-9.9,0))
        self.assertFalse(v8 != Vector(0.8,-0.3))
        #not equal
        self.assertTrue(v0 != v1)
        self.assertTrue(v2 != v3)
        self.assertTrue(v4 != v5)
        self.assertTrue(v6 != v7)
    
    def test_add(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
   
        self.assertEqual(v0 + v1, Vector(1.0,0.0))
        self.assertEqual(v4 + v8, Vector(0.8,-1.3))
        self.assertEqual(v8 + v4, Vector(0.8,-1.3)) # communative
        self.assertEqual(v3 + v8, Vector(-0.2,-0.3))
        self.assertEqual(v6 + v7, Vector(-3.9,-2.0))
        self.assertEqual(v7 + v5, Vector(-4.9,4.0))
        self.assertEqual(v3 + v3, Vector(-2.0,0.0))
        self.assertEqual(v2 + v1, Vector(1.0,1.0))
        
        v0 += [v1.x,v1.y]                           # list test
        v4 += v8
        v3 += v8
        v6 += v7
        v7 += v5
        
        self.assertEqual(v0, (1.0,0.0))
        self.assertEqual(v4, Vector(0.8,-1.3))
        self.assertEqual(v3, Vector(-0.2,-0.3))
        self.assertEqual(v6, Vector(-3.9,-2.0))
        self.assertEqual(v7, Vector(-4.9,4.0))
    
    def test_sub(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
   
        self.assertEqual(v0 - v1, Vector(-1.0,0.0))
        self.assertEqual(v4 - v8, Vector(-0.8,-0.7))
        self.assertNotEqual(v8 - v4, Vector(-0.8,-0.7)) # not communative
        self.assertEqual(v3 - v8, Vector(-1.8,0.3))
        self.assertEqual(v6 - v7, Vector(15.9,-2.0))
        self.assertEqual(v7 - v5, Vector(-14.9,-4.0))
        self.assertEqual(v3 - v3, Vector(0.0,0.0))           
        self.assertEqual(v2 - v1, Vector(-1.0,1.0))
        
        v0 -= [v1.x,v1.y]                                #list test
        v4 -= v8
        v3 -= v8
        v6 -= v7
        v7 -= v5
        
        self.assertEqual(v0, Vector(-1.0,0.0))
        self.assertEqual(v4, Vector(-0.8,-0.7))
        self.assertEqual(v3, Vector(-1.8,0.3))
        self.assertEqual(v6, Vector(15.9,-2.0))
        self.assertEqual(v7, Vector(-14.9,-4.0))
        
    def test_star(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
        
        v5 = (v5.x,v5.y)   #test tuple
        
        self.assertEqual( (v0) .star (v1), Vector(0.0,0.0))
        self.assertEqual( (v4) .star (v8), Vector(-0.3,-0.8))
        self.assertEqual( (v8) .star (v4), Vector(-0.3,-0.8)) # communative
        self.assertEqual( (v3) .star (v8), Vector(-0.8,0.3))
        self.assertEqual( (v6) .star (v7), Vector(-59.4,19.8))
        self.assertEqual( (v7) .star (v5), Vector(-49.5,-39.6)) #test tuple here
        self.assertEqual( (v3) .star (v3), Vector(1.0,0.0))            
        self.assertEqual( star(v2,v1), Vector(0.0,1.0))
    
    def test_dot(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
        
        v5 = (v5.x,v5.y)   #test tuple
        
        self.assertTrue(about_equal( (v0) .dot (v1), 0))
        self.assertTrue(about_equal( (v4) .dot (v8), 0.3))
        self.assertTrue(about_equal( (v8) .dot (v4), 0.3))        # communative
        self.assertTrue(about_equal( (v3) .dot (v8), -0.8))
        self.assertTrue(about_equal( (v6) .dot (v7), -59.4))
        self.assertTrue(about_equal( (v7) .dot (v5), -49.5)) #test tuple here
        self.assertTrue(about_equal( (v3) .dot (v3), 1))           
        self.assertTrue(about_equal( dot(v2,v1), 0))
        
        
    def test_cross(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
        
        v5 = (v5.x,v5.y)   #test tuple
        
        self.assertTrue(about_equal( (v0) .cross (v1), 0))
        self.assertTrue(about_equal( (v4) .cross (v8), 0.8)) 
        self.assertTrue(about_equal( (v8) .cross (v4), -0.8))    # negative communative
        self.assertTrue(about_equal( (v3) .cross (v8), 0.3))
        self.assertTrue(about_equal( (v6) .cross (v7), -19.8))
        self.assertTrue(about_equal( (v7) .cross (v5), -39.6))  #test tuple here
        self.assertTrue(about_equal( (v3) .cross (v3), 0))           
        self.assertTrue(about_equal( cross(v2,v1), -1))
        
        
    def test_mul_rmul(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
        
        self.assertEqual(v0 * 2, Vector(0.0,0.0))
        self.assertEqual(v3 * -0.1, Vector(0.1,0.0))
        self.assertEqual(v7 * -9.8, Vector(97.02,0.0))
        self.assertEqual(v4 * 4, Vector(0.0,-4.0))
        self.assertEqual(4 * v4, Vector(0.0,-4.0)) # communative
        self.assertEqual(9 * v5, Vector(45.0,36.0))
        self.assertEqual(-6 * v3, Vector(6.0,0.0))            
        self.assertEqual(0 * v1, Vector(0.0,0.0))
        
        v0 *= 2                            
        v3 *= -0.1
        v4 *= 4
        v7 *= -9.8
        v5 *= 9
        
        self.assertEqual(v0, Vector(0.0,0.0))
        self.assertEqual(v3, Vector(0.1,0.0))
        self.assertEqual(v4, Vector(0.0,-4.0))
        self.assertEqual(v7, Vector(97.02,0.0))
        self.assertEqual(v5, Vector(45.0,36.0))
    
    def test_div(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
        
        self.assertEqual(v0 / 2., Vector(0.0,0.0))
        self.assertEqual(v3 / -0.1, Vector(10.0,0.0))
        self.assertEqual(v7 / -9.8, Vector(1.01020408163265306122,0.0))
        self.assertEqual(v4 / 4, Vector(0.0,-0.25))

        
        v0 /= 2                            
        v3 /= -0.1
        v4 /= 4
        v7 /= -9.8
        
        self.assertEqual(v0, Vector(0.0,0.0))
        self.assertEqual(v3, Vector(10.0,0.0))
        self.assertEqual(v4, Vector(0.0,-0.25))
        self.assertEqual(v7, Vector(1.01020408163265306122,0.0))
    
    def test_abs(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
        
        self.assertEqual(abs(v0), Vector(0.0,0.0))
        self.assertEqual(abs(v1), Vector(1,0))
        self.assertEqual(abs(v2), Vector(0,1))
        self.assertEqual(abs(v3), Vector(1,0))
        self.assertEqual(abs(v4), Vector(0,1))
        self.assertEqual(abs(v5), Vector(5,4))
        self.assertEqual(abs(v6), Vector(6,2))
        self.assertEqual(abs(v7), Vector(9.9,0))
        self.assertEqual(abs(v8), Vector(0.8,0.3))

    
    def test_neg(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
        
        self.assertEqual(-v0, Vector(0.0,0.0))
        self.assertEqual(-v1, Vector(-1,0))
        self.assertEqual(-v2, Vector(0,-1))
        self.assertEqual(-v3, Vector(1,0))
        self.assertEqual(-v4, Vector(0,1))
        self.assertEqual(-v5, Vector(-5,-4))
        self.assertEqual(-v6, Vector(-6,2))
        self.assertEqual(-v7, Vector(9.9,0))
        self.assertEqual(-v8, Vector(-0.8,0.3))
    
    def test_invert(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        self.reset()
        
        self.assertEqual(~v0, Vector(0.0,0.0))
        self.assertEqual(~v1, Vector(1,0))
        self.assertEqual(~v2, Vector(0,-1))
        self.assertEqual(~v3, Vector(-1,0))
        self.assertEqual(~v4, Vector(0,1))
        self.assertEqual(~v5, Vector(5,-4))
        self.assertEqual(~v6, Vector(6,2))
        self.assertEqual(~v7, Vector(-9.9,0))
        self.assertEqual(~v8, Vector(0.8,0.3))
        
    def reset(self):
        global v0,v1,v2,v3,v4,v5,v6,v7,v8
        v0 = Vector(0,0)
        v1 = Vector(1,0)
        v2 = Vector(0,1)
        v3 = Vector(-1,0)
        v4 = Vector(0,-1)
        v5 = Vector(5,4)
        v6 = Vector(6,-2)
        v7 = Vector(-9.9,0)
        v8 = Vector(0.8,-0.3)
        
if __name__ == "__main__":
    print("vector.py")
    #unittest.main()
    