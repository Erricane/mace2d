from vector import *
from gjk import *


def conservative_advancement(shape1,shape2,vector):
    advancements = [Vector(0,0)]
    total_advancement = Vector(0,0)
    
    before_separation = gjk(shape2,shape1)[0]
    separation = decrease(before_separation,shape1.get_skin() + shape2.get_skin())
     
    if before_separation == Vector(0,0): #already colliding
        #advance fully
        shape1.position += vector
        total_advancement += vector
        advancements.append(total_advancement)
        return advancements
        
    iterations = 0
    while True:
        iterations += 1
        if iterations > 97:
            print(separation)
            print(gjk(shape2,shape1)[0],shape1.get_skin() + shape2.get_skin())
        if iterations > 100:
            print(gjk(shape2,shape1)[0],shape1.get_skin() + shape2.get_skin())
            print("\n")
            break
            
        sep_dot = dot(separation,vector)
        sep_sqr = sqr_norm(separation)
        before_sep_dot = dot(before_separation,vector)
        if dot(before_separation,vector) <= 0 : #vector is going the other way
            #advance fully
            shape1.position += vector
            total_advancement += vector
            advancements.append(total_advancement)
            
            #do not repeat
            break
            
        if sep_dot == 0: #not parallel (above case), must not be significant
            break
        
        if sep_dot > sep_sqr :
            #advance partly
            
            advancement = min(1,sep_sqr / sep_dot) * vector 
            pre_vector = vector
            vector -= advancement
            pre_position = shape1.position
            shape1.position += advancement
            if shape1.position == pre_position:
                #advancement is too small, doesn't count
                break
            total_advancement += advancement
            advancements.append(total_advancement)
            
            #repeat
            before_separation = gjk(shape2,shape1)[0]
            separation = decrease(before_separation,shape1.get_skin() + shape2.get_skin())
            
            if separation == Vector(0,0):
                return advancements
            

        else: 
            #advance fully
            shape1.position += vector
            total_advancement += vector
            advancements.append(total_advancement)

            #do not repeat
            break

    return advancements
    
