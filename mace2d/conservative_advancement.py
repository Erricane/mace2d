from vector import *
from gjk import *

def conservative_advancement(shape1,shape2,vector):
    advancements = []
    total_advancement = Vector(0,0)
    
    separation = gjk(shape2,shape1)
    
    while separation_significant(separation):
        separation_alongness = alongness(vector,separation[0])
        
        if separation_alongness > 1:
            #advance partly
            advancement = vector / separation_alongness
            vector -= advancement
            shape1.position += advancement
            total_advancement += advancement
            advancements.append(total_advancement)
            
            #repeat
            separation = gjk(shape2,shape1)

        else:
            #advance partly
            shape1.position += vector
            total_advancement += vector
            advancements.append(total_advancement)
            
            #do not repeat
            break

    return advancements
    
def separation_significant(separation):
    if separation[0] == None:
        return False
    if sqr_norm(separation[0]) < 1:
        return False
    return True