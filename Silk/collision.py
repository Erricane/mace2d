#Collision Algorithms
from collider import *
import numpy as np
import numpy.linalg as nplin
import unittest
#TODO add comments and make functions  to make gjk clearer    
def simplex_vector(simplex):
    #From B to A
    if len(simplex) == 1:
        return simplex[0]
    else:
        direction = simplex[1] - simplex[0]
        return simplex[0] + np.dot(-simplex[0],direction) * direction / (
            np.dot(direction,direction)
        )
    


def perpendicular(vector):
    return np.array([-vector[1],vector[0]])
    

def nearest_simplex(simplex):
    if len(simplex) == 3:
        direction20 = simplex[0] - simplex[2]
        direction21 = simplex[1] - simplex[2]
        perp20 = perpendicular(direction20)
        perp21 = perpendicular(direction21)
        to_origin = -simplex[2]
        
        #which vector is "right most"?
        #[LM,RM.POINT]
        if np.dot(perp20,direction21) > 0:
            leftmost = direction21
            rightmost = direction20
            perpleft = perp21
            perpright = -perp20
            #make simplex triangle in clockwise order
            swap = simplex[0]
            simplex[0] = simplex[1]
            simplex[1] = swap
            
        else:
            leftmost = direction20
            rightmost = direction21
            perpleft = perp20
            perpright = -perp21
            
        if np.dot(perpleft,to_origin) > 0:
            if np.dot(leftmost, to_origin) > 0:
                simplex = [simplex[0], simplex[2]]
                return simplex,perpleft,False
            else:
                simplex = [simplex[2]]
                return simplex,to_origin,False
        
        else:
            if np.dot(perpright,to_origin) > 0:
                if np.dot(rightmost,to_origin) > 0:
                    simplex = [simplex[1], simplex[2]]
                    return simplex,perpright,False
                else:
                    simplex = [simplex[2]]
                    return simplex,to_origin,False
        
            else:
                #return EPA instead of None?
                return simplex,None,True
                
             
        
    if len(simplex) == 2:
        direction = simplex[0] -simplex[1]
        to_origin = -simplex[1]
        if np.dot(to_origin, direction) < 0:
            simplex = [simplex[1]]
            return simplex, -simplex[0], False
        else:
            # For 3d: np.cross(np.cross(-direction,-simplex[1]),-direction)
            perp = perpendicular(direction)
            if np.dot(to_origin, perp) < 0:
                perp = -perp
            return simplex, perp, False
    
    if len(simplex) == 1:
        return simplex, -simplex[0], False
        
    raise ValueError("Simplex is too large")

def gjk_intersection(collider1, collider2):
    position1 = collider1.get_position()
    position2 = collider2.get_position()
    shape1 = collider.get_shape()
    shape2 = collider.get_shape()
    
    beam_vector = np.array([1,0])
    beam_point1 = shape1.get_beam_point(beam_vector) + position1
    beam_point2 = shape2.get_beam_point(-beam_vector) + position2
    
    beam_point = shape_beam_point1 - shape_beam_point2
    
    simplex = [beam_point]
    beam_vector = -beam_point
    iterations = 1
    while True:
        beam_point1 = shape1.get_beam_point(beam_vector) + position1
        beam_point2 = shape2.get_beam_point(-beam_vector) + position2
        beam_point = shape_beam_point1 - shape_beam_point2
        
        if np.dot(beam_point, beam_vector) < 0:
            #TODO replace conditional with whether beam point is almost equal to any point in the simplex
            return simplex_vector(simplex), simplex, iterations
    
        simplex.append(beam_point)
        simplex, beam_vector, contains_origin = nearest_simplex(simplex)
        if contains_origin:
            return 0, simplex, iterations
        
        iterations += 1

def vector_equals(vector1,vector2):
    return vector1[0] == vector2[0] and vector1[1] == vector2[1]
    
    
def simplex_equals(simplex1,simplex2):
    value = len(simplex1) == len(simplex2)
    if value:
        for i in range(len(simplex1)):
            value = value and vector_equals(simplex1[i],simplex2[i])
    return value

class Collision_Test(unittest.TestCase):
    
    def test_simplex_equals(self):
        simplex1 = [np.array([0,0])]
        simplex2 = [np.array([0,0])]
        self.assertTrue(simplex_equals(simplex1,simplex2))
        simplex2 = [np.array([0,1])]
        self.assertFalse(simplex_equals(simplex1,simplex2))
        simplex1 = [np.array([0,1])]
        self.assertTrue(simplex_equals(simplex1,simplex2))
        simplex2.append(np.array([5,6]))
        self.assertFalse(simplex_equals(simplex1,simplex2))
        simplex1.append(np.array([5,6]))
        self.assertTrue(simplex_equals(simplex1,simplex2))
        
        
    
    def test_simplex_vector(self):
        simplex = [np.array([0,0])]
        self.assertEqual(simplex_vector(simplex)[0], 0)
        self.assertEqual(simplex_vector(simplex)[1], 0)
        
        simplex = [np.array([1,-2])]
        self.assertEqual(simplex_vector(simplex)[0], 1)
        self.assertEqual(simplex_vector(simplex)[1], -2)
        
        simplex = [np.array([1,-2]),np.array([1,5])]
        self.assertEqual(simplex_vector(simplex)[0], 1)
        self.assertEqual(simplex_vector(simplex)[1], 0)
        
        simplex = [np.array([1,0]),np.array([0,1])]
        self.assertEqual(simplex_vector(simplex)[0], 0.5)
        self.assertEqual(simplex_vector(simplex)[1], 0.5)
        
    def test_nearest_simplex(self):
        s = [np.array([1,0])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([1,0])]))
        self.assertTrue(vector_equals(u,np.array([-1,0])))
        self.assertFalse(v)
        
        s = [np.array([1,1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([1,1])]))
        self.assertTrue(vector_equals(u,np.array([-1,-1])))
        self.assertFalse(v)
        
        s = [np.array([0,1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([0,1])]))
        self.assertTrue(vector_equals(u,np.array([0,-1])))
        self.assertFalse(v)
        
        s = [np.array([-1,1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([-1,1])]))
        self.assertTrue(vector_equals(u,np.array([1,-1])))
        self.assertFalse(v)
        
        s = [np.array([1,0])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([1,0])]))
        self.assertTrue(vector_equals(u,np.array([-1,0])))
        self.assertFalse(v)
        
        s = [np.array([1,1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([1,1])]))
        self.assertTrue(vector_equals(u,np.array([-1,-1])))
        self.assertFalse(v)
        
        s = [np.array([0,1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([0,1])]))
        self.assertTrue(vector_equals(u,np.array([0,-1])))
        self.assertFalse(v)
        
        s = [np.array([-1,1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([-1,1])]))
        self.assertTrue(vector_equals(u,np.array([1,-1])))
        self.assertFalse(v)
        
        s = [np.array([1,0]),np.array([0,1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([1, 0]), np.array([0, 1])]))
        self.assertTrue(vector_equals(u,np.array([-1, -1])))
        self.assertFalse(v)
        
        s = [np.array([1,0]),np.array([0,1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([1, 0]), np.array([0, 1])]))
        self.assertTrue(vector_equals(u,np.array([-1, -1])))
        self.assertFalse(v)
        
        s = [np.array([1,0]),np.array([0.25,0.25])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([ 0.25,  0.25])]))
        self.assertTrue(vector_equals(u,np.array([-0.25, -0.25])))
        self.assertFalse(v)
        
        s = [np.array([-1,1]),np.array([-1.5,-1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([-1,  1]), np.array([-1.5, -1. ])]))
        self.assertTrue(vector_equals(u,np.array([ 2. , -0.5])))
        self.assertFalse(v)
        
        s = [np.array([-1,1]),np.array([0.5,-1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([-1,  1]), np.array([ 0.5, -1. ])]))
        self.assertTrue(vector_equals(u,np.array([ 2. ,  1.5])))
        self.assertFalse(v)
        
        s = [np.array([1,1]),np.array([-1,1]),np.array([0.5,0.5])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([-1,  1]), np.array([ 0.5,  0.5])]))
        self.assertTrue(vector_equals(u,np.array([-0.5, -1.5])))
        self.assertFalse(v)
        
        s = [np.array([-1,1]),np.array([1,1]),np.array([0.5,0.5])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([-1,  1]), np.array([ 0.5,  0.5])]))
        self.assertTrue(vector_equals(u,np.array([-0.5, -1.5])))
        self.assertFalse(v)
        
        s = [np.array([1,1]),np.array([-1,1]),np.array([0,0.5])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([ 0. ,  0.5])]))
        self.assertTrue(vector_equals(u,np.array([-0. , -0.5])))
        self.assertFalse(v)
        
        s = [np.array([1,1]),np.array([-1,1]),np.array([-0.5,0.5])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([1, 1]), np.array([-0.5,  0.5])]))
        self.assertTrue(vector_equals(u,np.array([ 0.5, -1.5])))
        self.assertFalse(v)
        
        s = [np.array([-1,1]),np.array([1,1]),np.array([-0.5,0.5])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([1, 1]), np.array([-0.5,  0.5])]))
        self.assertTrue(vector_equals(u,np.array([ 0.5, -1.5])))
        self.assertFalse(v)
        
        s = [np.array([1,1]),np.array([-1,1]),np.array([0,-1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([-1,  1]), np.array([1, 1]), np.array([ 0, -1])]))
        self.assertEqual(u,None)
        self.assertTrue(v)
        
        s = [np.array([-1,1]),np.array([1,1]),np.array([0,-1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([-1,  1]), np.array([1, 1]), np.array([ 0, -1])]))
        self.assertEqual(u,None)
        self.assertTrue(v)
        
        s = [np.array([1,1]),np.array([-1,-1]),np.array([-1,1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([1,1]),np.array([-1,-1]),np.array([-1,1])]))
        self.assertEqual(u,None)
        self.assertTrue(v)
        
        s = [np.array([1,1]),np.array([-1,-1]),np.array([1,-1])]
        t,u,v = nearest_simplex(s)
        self.assertTrue(simplex_equals(t,[np.array([-1,-1]),np.array([1,1]),np.array([1,-1])]))
        self.assertEqual(u,None)
        self.assertTrue(v)
        
if __name__ == "__main__":
    collision_test_suite = unittest.TestLoader().loadTestsFromTestCase(Collision_Test)