from vector import *
from test_polygon_shape import *
from bounds import *
from conservative_advancement import *
import random as rd

class Body:
    
    def __init__(self):
        self.position = Vector(0,0)
        self.velocity = Vector(rd.randint(-10,10),rd.randint(-10,10))
        self.colliders = []
        
    def attach(self,collider):
        self.colliders.append(collider)
        collider.set_position(self.position)
        return self
        
    def get_colliders(self):
        return self.colliders
        
    def step(self,tick):
        hit_something = False
        advancement = tick * self.velocity
        advancement_sqr_norm = sqr_norm(advancement)
        for collider in self.colliders:
            c_advancement, c_advancement_sqr_norm  = collider.get_advancement(advancement,advancement_sqr_norm)
            if c_advancement_sqr_norm < advancement_sqr_norm:
                hit_something = True
                advancement = c_advancement
                advancement_sqr_norm = c_advancement_sqr_norm
                
        self.position += advancement
        
        for collider in self.colliders:
            collider.set_position(self.position)
        if hit_something:
            self.velocity = Vector(rd.randint(-10,10),rd.randint(-10,10))

            
        
class Collider:
    
    def __init__(self):
        self.shape = generate_polygon()
        self.broadphase = None
        
    def get_support(self,beam):
        return self.shape.get_support(beam)
        
    def get_skin(self):
        return 10
        
    def set_broadphase(self,broadphase):
        self.broadphase = broadphase
        
    def set_position(self,position):
        self.shape.set_position(position)
        
    def get_bounds(self):
        return self.shape.get_bounds().pad(self.get_skin())
        
    def draw(self,canvas):
        self.shape.draw(canvas,"red")
        
    def get_advancement(self,initial_advancement,initial_advancement_sqr_norm):
        initial_position = self.shape.get_position()
        advancement = initial_advancement
        advancement_sqr_norm = initial_advancement_sqr_norm
        bounds = self.get_bounds()
        sweeping_bounds = bounds.sweep(advancement)
        
        for collider in self.broadphase.get_colliders():
            if collider != self:
                if collider.get_bounds().intersects(sweeping_bounds):
                    c_advancement = conservative_advancement(self.shape,collider.shape,advancement)[-1]
                    c_advancement_sqr_norm = sqr_norm(c_advancement)
                    if c_advancement_sqr_norm < advancement_sqr_norm:
                        advancement = c_advancement
                        advancement_sqr_norm = c_advancement_sqr_norm
                        sweeping_bounds = bounds.sweep(advancement)
                    self.shape.set_position(initial_position)
        
        return advancement, advancement_sqr_norm

class Broadphase:
    
    def __init__(self):
        self.colliders = []
        
    def add_collider(self,collider):
        self.colliders.append(collider)
        collider.set_broadphase(self)
        
    def draw(self,canvas):
        for collider in self.colliders:
            collider.draw(canvas)
            
    def get_colliders(self):
        return self.colliders
        
class World:
    
    def __init__(self):
        self.bodys = []
        self.broadphase = Broadphase()
        
    def add_body(self, body):
        self.bodys.append(body)
        for collider in body.get_colliders():
            self.broadphase.add_collider(collider)
        
    def add_collideer(self, collider):
        self.broadphase.add(collider)
        
    def draw(self,canvas):
        self.broadphase.draw(canvas)
        
    def step(self,tick):
        for body in self.bodys:
            body.step(tick)
        
        
            