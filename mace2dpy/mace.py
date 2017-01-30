from vector import *
from test_polygon_shape import *
from bounds import *
from conservative_advancement import *
import random as rd

class Body:
    
    def __init__(self, user_data = None):
        self.position = Vector(0,0)
        self.velocity = Vector(0,0)
        self.user_data = user_data
        self.fixtures = []
        self.broadphase = None
        
        
    def set_velocity(self, velocity):
        self.velocity = velocity
        return self
        
    def set_position(self, position):
        self.position = position
        for fixture in self.fixtures:
            fixture.set_position(position)
        return self
    
    def set_user_data(self,user_data):
        self.user_data = user_data
        return self
        
    def get_user_data(self):
        return self.user_data
        
    def add_fixture(self,fixture):
        self.fixtures.append(fixture)
        fixture.set_position(self.position)
        fixture.body = self
        if self.broadphase != None:
            self.broadphase.add_fixture(fixture)
        
        return self
        
    def get_fixtures(self):
        return self.fixtures
        
    def advance(self,time_step,pre_advance_callback,post_advance_callback):
        advancement = time_step * self.velocity
        advancement_sqr_norm = sqr_norm(advancement)
        impact_fixture = None
        proxy_fixture = None      
        for fixture in self.fixtures:
            #c_ stands for current
            c_advancement, c_advancement_sqr_norm, c_impact_fixture  = (
                fixture.get_advancement(
                    advancement,
                    advancement_sqr_norm,
                    pre_advance_callback
                )
            )
            
            
            #if we've hit something, reduce advancement
            if c_advancement_sqr_norm < advancement_sqr_norm:
                advancement = c_advancement
                advancement_sqr_norm = c_advancement_sqr_norm
                impact_fixture = c_impact_fixture
                proxy_fixture = fixture
                
        self.position += advancement
        
        for fixture in self.fixtures:
            fixture.set_position(self.position)
        if impact_fixture != None:
            post_advance_callback(proxy_fixture,impact_fixture)
            

class Fixture:
    
    def __init__(self, shape, user_data = None):
        self.shape = shape
        self.user_data = user_data
        self.broadphase = None
        self.body = None
        
    def get_support(self,beam):
        return self.shape.get_support(beam)
        
    def get_skin(self):
        return 0
        
    def get_body(self):
        return self.body
        
    def set_position(self,position):
        self.shape.set_position(position)
        return self
        
    def set_user_data(self,user_data):
        self.user_data = user_data
        return self
        
    def get_user_data(self):
        return self.user_data
        
    def get_bounds(self):
        return self.shape.get_bounds().pad(self.get_skin())
        
    def draw(self,canvas):
        self.shape.draw(canvas,"red")
        
    def get_advancement(
        self,
        initial_advancement,
        initial_advancement_sqr_norm,
        pre_advance_callback
    ):
        initial_position = self.shape.get_position()
        advancement = initial_advancement
        advancement_sqr_norm = initial_advancement_sqr_norm
        bounds = self.get_bounds()
        sweeping_bounds = bounds.sweep(advancement)
        impact_fixture = None
        for fixture in self.broadphase.get_fixtures():
            if fixture.body != self.body:
                if fixture.get_bounds().intersects(sweeping_bounds):
                    if pre_advance_callback(self,fixture) == IMPACT:
                        #c_ stands for current
                        c_advancement = conservative_advancement(self.shape,fixture.shape,advancement)[-1]
                        c_advancement_sqr_norm = sqr_norm(c_advancement)
                        if c_advancement_sqr_norm < advancement_sqr_norm:
                            impact_fixture = fixture
                            advancement = c_advancement
                            advancement_sqr_norm = c_advancement_sqr_norm
                            sweeping_bounds = bounds.sweep(advancement)
                        self.shape.set_position(initial_position)
        
        return advancement, advancement_sqr_norm, impact_fixture

class Broadphase:
    
    def __init__(self):
        self.fixtures = []
        
    def add_fixture(self,fixture):
        if fixture.broadphase != self:
            self.fixtures.append(fixture)
            fixture.broadphase = self
        
    def draw(self,canvas):
        for fixture in self.fixtures:
            fixture.draw(canvas)
            
    def get_fixtures(self):
        return self.fixtures
        
class World:
    
    def __init__(self):
        self.bodys = []
        self.broadphase = Broadphase()
        self.pre_advance_callback = always_ignore
        self.post_advance_callback = do_nothing
        
    def set_pre_advance_callback(self, pre_advance_callback):
        self.pre_advance_callback =  pre_advance_callback
        return self
    
    def set_post_advance_callback(self, post_advance_callback):
        self.post_advance_callback = post_advance_callback
        return self
        
    def create_body(self):
        body = Body()
        
        self.bodys.append(body)

        body.broadphase = self.broadphase
        for fixture in body.fixtures:
            self.broadphase.add_fixture(fixture)
        return body
        
    def create_fixture(self):
        fixture = Fixture()
        self.broadphase.add(fixture)
        return fixture
        
        
    def add_body(self, body):
        self.bodys.append(body)
        if body.broadphase != self.broadphase:
            #don't add body twice
            body.broadphase = self.broadphase
            for fixture in body.fixtures:
                self.broadphase.add_fixture(fixture)
            return self
        
    def add_fixture(self, fixture):
        self.broadphase.add(fixture)
        return self
        
    def draw(self,canvas):
        self.broadphase.draw(canvas)
        
    def step(self,time_step):
        for body in self.bodys:
            body.advance(time_step,self.pre_advance_callback,self.post_advance_callback)
 
        
def always_ignore(fixture1, fixture2):
    return IGNORE
    
def do_nothing(fixture1, fixture2):
    pass
            
def always_impact(fixture1, fixture2):
    return IMPACT
    
def always_stop(fixture1, fixture2):
    print("Collision")
    fixture1.get_body().set_velocity(Vector(0,0))
    fixture2.get_body().set_velocity(Vector(0,0))
    
    
#Collision:
#Advancement
#Colliders
#Search Size
#Sensing bounding box padding

#7 types of motion rotation/linear, pre(linear), velocity, shift(use a different workd?), jump

#Search steps with custom or extra broadphases

#there is "advance" and "survey", together, they make step.

#Collision stops advancement (conservative advancement)
#Response calls callback for pass_throughs or collisions, 
#current motion, current iteration
IGNORE = 0      #No Collision, whatsoever
PASS  = 1       #No Collision, Has Response, for sweeping movement
IMPACT = 2      #Collision and Response, Rename to BLOCK? IMPACT?
WAIT_PASS = 3   #If possible, waits for the object to move out of the way before processing it again, otherwise, pass it
WAIT_COLLIDE=4  #If possible, waits for the object to move out of the way before processing it again, otherwise, fixture

#Separation required for stay, 0 means colliding, negative means ignore,

#Response (needs to know if it was a pass or collide or stay and type of motion
#DEFLECT (Relative/Absolute/Ignore,Bounce,BounceReduce,BounceMinimum,Slide,SlideReduce,SlideMinimum,PreSlide,iterations)
#FROM_DEFLECT (vectors results from deflect, no effect on the bodys)
#Bounce and slide (see deflect)
#STOP (Relative, Absolute, Ignore)
#RotationSTOP
#FROM_STOP (vector results from stop, no effect on the bodies)
#FORCE_OUT (one, both, ratio) No checks, EPA's one out of the other, no velcity change
#MOVE_OUT (one, both, ratio) EPA out next step using velocity change of displacement
#FROM_SEPARATION (use EPA or not?)
#FROM_FORCE_OUT
#FROM_MOVE_OUT
#APPLY (Vectors, preApply, iterations)
#ADD (Vectors, preAdd, iterations)
#REJECT (False) or ACCEPT (True)

#Custom Stepping (out-of-world body step, can not change other bodies, offers means of cancelling(Reject))
#custom sensoring (out-of-world body sense, can not change other bodies, offers means of cancelling(Reject))

#Binding body's together