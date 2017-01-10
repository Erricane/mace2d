import tkinter as tk
from test_polygon_shape import *
from gjk import *
from conservative_advancement import *
import random as rd
import numpy as np


def reset(event = None):
    global canvas, root, poly1, poly2, target

    poly1 = generate_polygon()
    poly2 = generate_polygon()
    target = Vector(400,400)
    poly2.position = Vector(400,400)
    draw()
    
def move_poly1(event):
    global canvas, root, poly1, poly2, target
    poly1.position = Vector(event.x,event.y)
    draw()
    
def move_target(event):
    global canvas, root, poly1, poly2, target
    target = Vector(event.x,event.y)
    draw()
    
def draw():
    global canvas, root, poly1, poly2, target
    
    canvas.delete(tk.ALL)
    
    position1 = poly1.position
    advancements = conservative_advancement(poly1,poly2, target - position1)
    poly1.position = position1
    
    color = "blue"
    outline = ""
    
    poly1.draw(canvas,color,outline)
    poly2.draw(canvas,color,outline)

    color = ""
    outline = "black"
    
    for advancement in advancements:
        poly1.position = advancement + position1
        poly1.draw(canvas,color,outline)
        
    poly1.position = position1
        

rd.seed(1)
np.random.seed(1)
root = tk.Tk()
canvas = tk.Canvas(root, width = 800, height = 800)
canvas.pack()
reset()
root.bind("<Return>",reset)  
root.bind("<B1-Motion>", move_poly1)
root.bind("<B3-Motion>", move_target)
root.mainloop()

