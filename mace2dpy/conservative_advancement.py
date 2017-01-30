from vector import *
from gjk import *


def conservative_advancement(shape1,shape2,vector):
    advancements = [Vector(0,0)]
    total_advancement = Vector(0,0)
    
    raw_separation = separation(shape1,shape2)[0]
    reduced_separation = decrease(raw_separation,shape1.get_skin() + shape2.get_skin())
     
    if raw_separation == Vector(0,0): #already colliding, not effect
        #advance fully
        shape1.position += vector
        total_advancement += vector
        advancements.append(total_advancement)
        return advancements
        
    iterations = 0
    while True:
        iterations += 1
        if iterations > 97:
            print(reduced_separation)
            print(separation(shape1,shape2)[0],shape1.get_skin() + shape2.get_skin())
        if iterations > 100:
            print(separation(shape1,shape2)[0],shape1.get_skin() + shape2.get_skin())
            print("\n")
            break
            
        sep_dot = dot(reduced_separation,vector)
        sep_sqr = sqr_norm(reduced_separation)
        before_sep_dot = dot(raw_separation,vector)
        if dot(raw_separation,vector) <= 0 : #vector is going the other way
            #advance fully
            shape1.position += vector
            total_advancement += vector
            advancements.append(total_advancement)
            return advancements
            
        if sep_dot == 0: #not parallel (above case) and must not be significant advancement, stop advancing
            return advancements
        
        if sep_dot > sep_sqr :
            #advance partly
            advancement = min(1,sep_sqr / sep_dot) * vector 
            pre_vector = vector
            vector -= advancement
            pre_position = shape1.position
            shape1.position += advancement
            total_advancement += advancement
            advancements.append(total_advancement)
            
            #repeat if we made progress with advancement
            old_raw_separation = raw_separation
            raw_separation = separation(shape1,shape2)[0]
            
            #we didn't make any progess, stop advancing 
            if old_raw_separation == raw_separation: 
                return advancements
            reduced_separation = decrease(raw_separation,shape1.get_skin() + shape2.get_skin())
            
            #we don't expect to make any more progress
            if reduced_separation == Vector(0,0):
                return advancements
            

        else: 
            #advance fully
            shape1.position += vector
            total_advancement += vector
            advancements.append(total_advancement)

            #do not repeat
            return advancements

    return advancements
    
