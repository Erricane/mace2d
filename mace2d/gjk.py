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
    

    
    #simplex is a clockwise-order triangle 
    if len(simplex) == 3:
        
        #from 2 to 0, leftmost vector
        left_direction20 = simplex[0] - simplex[2]  
        
        #from 2 to 1, rightmost vector
        right_direction21 = simplex[1] - simplex[2] 

        #from newest point to origin
        to_origin = -simplex[2]                      
        
        if leftof(to_origin, left_direction20) :    #origin is left of left_direction20, not in simplex           
            if along(to_origin, left_direction20):   
                simplex = [simplex[0], simplex[2]]  #left_direction20 is new simplex, CW order
                return simplex,left_perp(left_direction20),False
            else:                                       
                simplex = [simplex[2]]              
                return simplex,to_origin,False
        
        else:
            if rightof(to_origin, right_direction21):   #origin is right of right_direction21, not in simplex
                if along(right_direction21,to_origin):  
                    simplex = [simplex[2], simplex[1]]  #right_direction21 is new simplex, CW order
                    return simplex,right_perp(right_direction21),False
                else:                                   #origin against direction of right_direction21
                    simplex = [simplex[2]]
                    return simplex,to_origin,False
        
            else:
                return simplex,None,True

    #simplex is line
    if len(simplex) == 2:
        direction10 = simplex[0] -simplex[1]
        to_origin = -simplex[1]
        
        if against(to_origin, direction10):    
            simplex = [simplex[1]]
            return simplex, to_origin, False
            
        else:  
            #NOTE: Simplex must be in clockwise order when new point is added
            
            if rightof(to_origin, direction10):      
                simplex = [simplex[1], simplex[0]] #simplex is CW order 
                return simplex, right_perp(direction10), False
                
            else:
                #simplex already in CW order
                 return simplex, left_perp(direction10), False
    
    #simplex is a point
    if len(simplex) == 1:
        return simplex, -simplex[0], False
        
    raise ValueError("Simplex is too large")

def simplex_contains(simplex,support):
    for vec in simplex:
        if vec == support:
            return true
        else:
            return false

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
        if old_support == support: 
            return vector_to_origin(simplex), simplex, iterations
    
        #else expand simplex with support
        simplex.append(support)
        
        #get solution and nearest simplex to origin
        simplex, beam, contains_origin = simplex_process(simplex)
        iterations += 1
        
        if contains_origin:
            return None, simplex, iterations
        
        

