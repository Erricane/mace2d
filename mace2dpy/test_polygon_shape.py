from scipy.spatial import ConvexHull
import random as rd
import numpy as np
from vector import *
from bounds import * 

def generate_polygon(min = 1 ,max = 6):
    scale = rd.uniform (50,300)
    point_count = rd.randint(min,max)
    points = np.random.rand(point_count,2)
    if len(points) > 2:
        vertices = ConvexHull(points).vertices
    else:
        vertices = list(range(len(points)))
        
    convex_polygon_points = []    
    
    # create convex polygon and
    # convert from ndarray and numpy.float64 to standard
    for vertice in vertices:
        convex_polygon_points.append(
            Vector(
                scale * float(points[vertice][0]),
                scale * float(points[vertice][1])
            )
        )
        
    # subtract mean to center polygon around 0,0
    mean = Vector(0,0)
    count = 0
    for vector in convex_polygon_points:
        mean += vector
        count += 1
    mean /= count
    for vector_idx in range(len(convex_polygon_points)):
        convex_polygon_points[vector_idx] -= mean    
    
    return Polygon(convex_polygon_points)
        
    

class Polygon:
    
    def __init__(self,convex_polygon_points):
        self.points = convex_polygon_points
        self.position = Vector(0,0)
        
        left = self.points[0].x
        bottom = self.points[0].y
        right = self.points[0].x
        top = self.points[0].y
        
        for point in self.points:
            if point.x < left:
                left = point.x
            elif point.x > right:
                right = point.x
                
            if point.y < bottom:
                bottom = point.y
            elif point.y > top:
                top = point.y
            
        self.bounds = Bounds(Vector(left,bottom), Vector(right-left,top-bottom))
        
        
    def get_support(self, beam):
        support = self.points[0]
        along_factor = dot(beam,support) #along_factor is proportional to alongness
        for point in self.points:
            if dot(beam,point) > along_factor:
                support = point
                along_factor = dot(beam,support)
        return support + self.position
    
    def draw(self,canvas,color,outline = ""):
        drawing_points = []
        
        for point in self.points:
            drawing_points.append(list(point + self.position))
            
        #draw polygon
        if len(drawing_points) > 2:
            canvas.create_polygon(drawing_points,fill = color, outline = outline)
        elif len(drawing_points) == 2:
            canvas.create_line(drawing_points, fill =color+outline)
        else:
            canvas.create_oval(
                drawing_points[0][0] -3,
                drawing_points[0][1] -3,
                drawing_points[0][0] +3,
                drawing_points[0][1] +3,
                fill =color,
                outline = outline
            )
            
        #draw bounds
        canvas.create_rectangle(
            self.get_bounds().left(),
            self.get_bounds().bottom(),
            self.get_bounds().right(),
            self.get_bounds().top()
        )
            
    def get_position(self):
        return self.position
    
    def set_position(self, position):
        self.position = position
    
    def get_bounds(self):
        return self.bounds.offset(self.position)
        
    def get_skin(self):
        return 1.0