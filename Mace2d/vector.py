class Vector:
    
    def __init__(self,x = 0., y = 0.):
        self.x = float(x)
        self.y = float(y)
            
    def copy(self):
        return Vector(self.x, self.y)
        
    def __repr__(self):
        return (
            "vector(" +
            str(self.x) + "," +
            str(self.y) + ")"
        )
            
    def __eq__(self,other):
        return (
            self.x == other.x and 
            self.y == other.y
        )

    def __ne__(self,other):
        return (
            self.x != other.x or 
            self.y != other.y
        )
        
    def __add__(self,other):
        return Vector(
            self.x + other.x,
            self.y + other.y
        )
        
    def __sub__(self,other):
        return Vector(
            self.x - other.x,
            self.y - other.y
        )
        
    def __mul__(self,other):
        try:
            return Vector(
                self.x * other.x,
                self.y * other.y
            )
        except:
            return Vector(
                self.x * other,
                self.y * other
            )
            
    def __rmul__(self,other):
        try:
            return Vector(
                self.x * other.x,
                self.y * other.y
            )
        except:
            return Vector(
                self.x * other,
                self.y * other
            )
        
    def __abs__(self,other):
        return Vector(abs(self.x), abs(self.y))
        
    def __xor__(self,other):
        return self.x * other.y - self.y * other.x

    def __neg__(self):
        return Vector(-self.x, -self.y)

        
import unittest       
class Vector_Test(unittest.TestCase):
    
    def test_eq_ne(self):
        v0 = Vector(2,3)
        v1 = Vector(2.0,3.0)
        v2 = Vector(2.1,3.1)
        v3 = Vector(-2,-3)
        self.assertEqual(v0, v1)
        self.assertTrue(v0 == v1)
        self.assertTrue(v1 == v0)
        self.assertFalse(v2 == v1)
        self.assertFalse(v3 == v0)
        v3 = v0
        self.assertFalse(v3 != v0)
        v2 = v0.copy()
        self.assertFalse(v2 != v1)
        
    
    def test_add_sub_neg_copy(self):
        v0 = Vector(2,3)
        v1 = Vector(0,0)
        v2 = Vector(-1,3.1)
        v3 = Vector(2,0)
        v4 = v0 + v1
        self.assertEqual(v4, v0)
        self.assertEqual(v3+v0, Vector(4,3))
        self.assertEqual(v2 + (-v2), v1)
        self.assertEqual(v2 -v2, v1)
        v3 += v3
        v0 -= v0
        self.assertEqual(v3,Vector(4,0))
        self.assertEqual(v0,v1)
        v0 += v2
        self.assertEqual(v0,Vector(-1,3.1))
        v5 = Vector(4,0)
        v2 = v5.copy()
        v5 += v2
        self.assertEqual(v0,Vector(-1,3.1))
        self.assertEqual(v2,Vector(4,0))
        
        
    def test_mul(self):
        v0 = Vector(2,3)
        v1 = Vector(0,0)
        v2 = Vector(-1,3.1)
        v3 = Vector(2,0)
        v4 = v3 * 2
        self.assertEqual(v0 * v1, v1)
        self.assertEqual(v4, Vector(4,0))
        self.assertEqual(v0 * 0, Vector(0,0))
        self.assertEqual(v3*v0, v4)
        v0 *= 2
        v6 = Vector(0,2)
        v6 *= v3
        v3 *= v4
        self.assertEqual(v0,Vector(4,6))
        self.assertEqual(v1,v6)
        self.assertEqual(v3,Vector(8,0))
        
    def test_cross(self):
        v1 = Vector(0,0)
        v2 = Vector(1,0)
        v3 = Vector(0,1)
        v4 = Vector(2,3)
        self.assertEqual(v1^v4,0)
        self.assertEqual(v2^v3,1)
        self.assertEqual(v4^v3,-(v3^v4))
        self.assertEqual(v4^v3,2)
        
        
        
if __name__ == "__main__":
    unittest.main()
    