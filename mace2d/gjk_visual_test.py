import tkinter as tk
from test_polygon_shape import *
from gjk import *

def reset(event = None):
    global canvas, root, poly1, poly2
    poly1 = generate_polygon()
    poly2 = generate_polygon()
    poly2.position = Vector(400,400)
    draw()
    
def move_poly1(event):
    global canvas, root, poly1, poly2
    poly1.position = Vector(event.x,event.y)
    draw()
    
def draw():
    global canvas, root, poly1, poly2
    
    canvas.delete(tk.ALL)
    
    solution = gjk(poly1,poly2)
    
    color = "red"
    
    if solution[0] != None: 
        color = "blue"
        from1 = poly1.get_support(-solution[0])
        from2 = poly2.get_support(solution[0])
        to1 = from1 - solution[0]
        to2 = from2 + solution[0]
        canvas.create_line(
            list(from1),
            list(to1)
        )
        canvas.create_line(
            list(from2),
            list(to2)
        )
        
    poly1.draw(canvas,color)
    poly2.draw(canvas,color)

    
root = tk.Tk()
canvas = tk.Canvas(root, width = 800, height = 800)
canvas.pack()
reset()
root.bind("<Return>",reset)  
root.bind("<B1-Motion>", move_poly1)
root.mainloop()



