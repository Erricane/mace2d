import tkinter as tk
from test_polygon_shape import *
from gjk import *
from conservative_advancement import *
from mace import *
import random as rd
import numpy as np


def reset(event = None):
    global canvas, root, w
    w = World()
    
def create_body(event):
    global canvas, root, w
    b = Body()
    b.position = Vector(event.x,event.y)
    b.attach(Collider())
    w.add_body(b)
    draw()
    
def world_step(event):
    global canvas, root, w
    w.step(1)
    for body in w.bodys:
        if body.position.x >= 800:
            body.position.x = 800
            body.velocity = Vector(rd.randint(-10,10),rd.randint(-10,10))
        if body.position.x <= 0:
            body.position.x = 0
            body.velocity = Vector(rd.randint(-10,10),rd.randint(-10,10))
        if body.position.y >= 800:
            body.position.y = 800
            body.velocity = Vector(rd.randint(-10,10),rd.randint(-10,10))
        if body.position.y <= 0:
            body.position.y = 0
            body.velocity = Vector(rd.randint(-10,10),rd.randint(-10,10))
        if body.velocity == Vector(0,0):
            body.velocity = Vector(rd.randint(-10,10),rd.randint(-10,10))
    draw()
    
def print_body_velocity(event):
    global canvas, root, w
    for body in w.bodys:
        print(body.velocity)
    
def draw():
    global canvas, root, w
    canvas.delete(tk.ALL)
    w.draw(canvas)
        

rd.seed(1)
np.random.seed(1)
root = tk.Tk()
canvas = tk.Canvas(root, width = 800, height = 800)
canvas.pack()
reset()
root.bind("<Return>",reset)  

root.bind("<Button-1>", create_body)
root.bind("<B3-Motion>", world_step)
root.bind("<z>", world_step)
root.bind("<space>", print_body_velocity)
root.mainloop()

