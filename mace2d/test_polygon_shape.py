from scipy.spatial import ConvexHull
import random as rd
import numpy as np
from vector import *

def generate_polygon():
    scale = rd.uniform (50,300)
    point_count = rd.randint(1,6)
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
        
    # subtract mean to center 
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
        
    def get_support(self, beam):
        support = self.points[0]
        along_factor = dot(beam,support) #along_factor is proportional to alongness
        for point in self.points:
            if dot(beam,point) > along_factor:
                support = point
                along_factor = dot(beam,support)
        return support + self.position
    
    def draw(self,canvas,color):
        drawing_points = []
        for point in self.points:
            drawing_points.append(list(point + self.position))
            
            
        if len(drawing_points) > 2:
            canvas.create_polygon(drawing_points,fill = color)
        elif len(drawing_points) == 2:
            canvas.create_line(drawing_points, fill =color)
        else:
            canvas.create_oval(
                drawing_points[0][0] -3,
                drawing_points[0][1] -3,
                drawing_points[0][0] +3,
                drawing_points[0][1] +3,
                fill =color
            )