from vector import *


def vector_to_origin(simplex):
    #From shape2 to shape2


    #simplex is a point
    if len(simplex) == 1: 
        return simplex[0]
    
    #simplex is a line, return closes point from simplex to origin
    else:
        direction01 = simplex[1] - simplex[0]  
        return simplex[0] - project(simplex[0],direction01)
        

    

def simplex_process(simplex):
    # CCW means counter-clockwise

    #simplex is a CCW order triangle 
    if len(simplex) == 3:
        
        #from 2 to 0, rightmost vector
        right_direction20 = simplex[0] - simplex[2]  
        
        #from 2 to 1, leftmost vector
        left_direction21 = simplex[1] - simplex[2] 

        #from newest point to origin
        to_origin = -simplex[2]               
        
        
        if leftof(to_origin, right_direction20): #right segment is not closest
            if rightof(to_origin, left_direction21): #origin in triangle
                return simplex,None,True
            if along(to_origin, left_direction21): #left segment is closest 
                simplex = [simplex[2], simplex[1]]  #left_direction21 is new simplex, CCW order
                return simplex,left_perp(left_direction21),False
        else:
            if along(to_origin, right_direction20): #right segment is closest
                simplex = [simplex[0], simplex[2]]  #right_direction21 is new simplex, CCW order
                return simplex,right_perp(right_direction20),False
            if along(to_origin, left_direction21): #left segment is closest 
                simplex = [simplex[2], simplex[1]]  #left_direction21 is new simplex, CCW order
                return simplex,left_perp(left_direction21),False
        simplex = [simplex[2]]                      #origin is closest to new point   
        return simplex,to_origin,False


    #simplex is line
    elif len(simplex) == 2:
        direction10 = simplex[0] -simplex[1]
        to_origin = -simplex[1]
        
        #NOTE: Simplex must be in CCW order when new point is added
        if along(to_origin, direction10):
        
            if leftof(to_origin, direction10):      
                simplex = [simplex[1], simplex[0]] #simplex is CCW order 
                return simplex, left_perp(direction10), False
            
            #origin right of segment, simplex already in CCW order
            return simplex, right_perp(direction10), False
        
        #newest point is closest to origin
        simplex = [simplex[1]]
        return simplex, to_origin, False
             
    #simplex is a point
    elif len(simplex) == 1:
        return simplex, -simplex[0], False
        
    raise ValueError("Simplex is too large") 
    

def simplex_contain(simplex,support):
    if simplex[0] == support:
        return True
    if len(simplex) == 2:
        if simplex[1] == support:
            return True
    return False


def gjk(shape1, shape2):
    beam = Vector(1,0)
    
    #support means the furthest point in a (combined) shape in the beam direction
    support = shape1.get_support(beam) - shape2.get_support(-beam)
    
    simplex = [support]
    
    beam = -support
    iterations = 0
    
    while True:
        old_support = support
        support = shape1.get_support(beam) - shape2.get_support(-beam)
        
        #there is no closer point (from combined shape to the origin)
        if simplex_contain(simplex, support): 
            return vector_to_origin(simplex), simplex, iterations
    
        #else expand simplex with support
        simplex.append(support)
        
        #get solution and nearest simplex to origin
        simplex, beam, contains_origin = simplex_process(simplex)
        iterations += 1
        
        if contains_origin:
            return Vector(0,0), simplex, iterations
        
        if iterations > 100:
            raise ValueError(str(simplex) + "\n" + str(old_support) + "\n" + str(support))
        

def separation(shape1, shape2):
    #from A to B
    return gjk(shape2, shape1)
