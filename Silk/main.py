from collision_space import *
from list import *
from collider import *
from shape import *
from body import *
import numpy as np
import tkinter as tk
import tkinter.messagebox as msg
import tkSimpleDialog

print("main")


"""
c = Collider(np.array([-1,3]),basic_shape)
c.join(cs)

Collider(np.array([11,3]),basic_shape).join(cs)
print(cs.hash_grid)
c = c.empty()
print(cs.hash_grid)

b = Bounds(np.array([50,50]),np.array([9,1]))
list(cs.Collision_Space_Iterator(b))
"""


class App:
    def __init__(
        self, 
        width_in_cells = 10,
        height_in_cells = 10, 
        cell_width = 10, 
        cell_height = 10
    ):
        self.collision_space = Collision_Space(
            width_in_cells,
            height_in_cells,
            cell_width,
            cell_height
        )
        
        self.grid_lines_list = Smart_List()
        self.collider_list = Smart_List()
        
        master = tk.Tk()
        
        canvas = tk.Canvas(master, width = 500, height = 100)
        canvas.pack(side="top", fill="both", expand=True)
        
        self.master = master
        self.canvas = canvas
        
        canvas.bind("<Enter>", self.update_canvas)
        canvas.bind("<Button-1>", self.mouse_pressed)
        canvas.bind("<B1-Motion>",self.mouse_moved)
        canvas.bind("<ButtonRelease-1>", self.mouse_released)
        canvas.bind("<Button-3>", self.create_collider)
        self.selection = [0,0,0,0]
        self.selection_on = False
        
        master.mainloop()
        

        
    def mouse_pressed(self, event):
        self.selection[0] = event.x
        self.selection[1] = event.y
        self.selection[2] = event.x
        self.selection[3] = event.y
        self.selection_on = True
        self.update_canvas()
        
    def mouse_moved(self,event):
        self.selection[2] = event.x
        self.selection[3] = event.y
        self.update_canvas()
    
        
    def mouse_released(self,event):
        self.selection_on = False
        self.update_canvas()
        
    def update_canvas(self, event= None):
        self.canvas.delete(tk.ALL)
        if self.selection_on:
            self.draw_selected_cells(
                self.selection[0],
                self.selection[1],
                self.selection[2],
                self.selection[3]
            )
            self.draw_selected_colliders(
                self.selection[0],
                self.selection[1],
                self.selection[2],
                self.selection[3]
            )
            self.canvas.create_rectangle(
                self.selection[0],
                self.selection[1],
                self.selection[2],
                self.selection[3]
            )
        else:
            self.draw_colliders()
        self.draw_grid_lines()
        self.canvas.update_idletasks()
        
    def create_collider(self,event):
        x = event.x
        y = event.y
        try:
            name = Query(self.master,"Name").result
            left = float(Query(self.master,"Left").result)
            top = float(Query(self.master,"Top").result)
            right = float(Query(self.master,"Right").result)
            bottom = float(Query(self.master,"Bottom").result)
        
        except:
            msg.showwarning("","Cancelling Collider Creation!")
            return None
            
        collider = Collider(
            Body(np.array([x,y])),
            Rectangle(left, top, right, bottom)
        )
        self.collider_list.add(Entry(name,collider))
        collider.join(self.collision_space)
    
    def draw_selected_colliders(self,x1,y1,x2,y2):
        selection_bounds = Bounds(np.array([x1,y1]),np.array([x2-x1,y2-y1]))

        for collider in self.collision_space.Collision_Space_Iterator(
                selection_bounds
        ):
            collider_bounds = collider.get_bounds()
            collider_position = collider.get_position()
            if collider_bounds.intersects(selection_bounds):
                self.canvas.create_rectangle(
                    collider_bounds.get_left(),
                    collider_bounds.get_top(),
                    collider_bounds.get_right(),
                    collider_bounds.get_bottom(),
                    fill = "red"
                )
                self.canvas.create_oval(
                    collider_position[0] - 1,
                    collider_position[1] - 1,
                    collider_position[0] + 1,
                    collider_position[1] + 1,
                    fill = "black"
                )
            else:
                self.canvas.create_rectangle(
                    collider_bounds.get_left(),
                    collider_bounds.get_top(),
                    collider_bounds.get_right(),
                    collider_bounds.get_bottom(),
                    fill = "blue"
                )
                self.canvas.create_oval(
                    collider_position[0] - 1,
                    collider_position[1] - 1,
                    collider_position[0] + 1,
                    collider_position[1] + 1,
                    fill = "black"
                )
            
    def draw_colliders(self):
        for entry in self.collider_list:
            collider = entry.get_value()
            collider_bounds = collider.get_bounds()
            collider_position = collider.get_position()
            self.canvas.create_rectangle(
                collider_bounds.get_left(),
                collider_bounds.get_top(),
                collider_bounds.get_right(),
                collider_bounds.get_bottom(),
                fill = "red"
            )
            self.canvas.create_oval(
                collider_position[0] - 1,
                collider_position[1] - 1,
                collider_position[0] + 1,
                collider_position[1] + 1,
                fill = "black"
            )
        
        
    def draw_selected_cells(self,x1,y1,x2,y2):
        cell_width = self.collision_space.get_cell_width()
        cell_height = self.collision_space.get_cell_height()
        width_in_cells = self.collision_space.get_width_in_cells()
        height_in_cells = self.collision_space.get_height_in_cells()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        collision_space_width = cell_width * width_in_cells
        collision_space_height = cell_height * height_in_cells
        
        for x_index, y_index in (   
            self.collision_space.Collision_Space_Index_Iterator( 
                Bounds(np.array([x1,y1]),np.array([x2-x1,y2-y1]))
            )
        ):
            x_start = x_index * cell_width
            
            while x_start < canvas_width:
                y_start = y_index * cell_height
                while y_start < canvas_height:
                    self.canvas.create_rectangle(
                        x_start,
                        y_start,
                        x_start + cell_width,
                        y_start + cell_height,
                        fill = "gray"
                    )
                    y_start += collision_space_height
                x_start += collision_space_width
            
        
            
        
    def draw_selection(self,x1,y1,x2,y2):
        if x2 < x1:
            temp = x1
            x1 = x2
            x2 = temp
            
        if y2 < y1:
            temp = y1
            y1 = y2
            y2 = temp
            
        self.canvas.create_rectangle(x1,y1,y1,y2,outline = "blue")
        
    def draw_grid_lines(self):
        cell_width = self.collision_space.get_cell_width()
        cell_height = self.collision_space.get_cell_height()
        width_in_cells = self.collision_space.get_width_in_cells()
        height_in_cells = self.collision_space.get_height_in_cells()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        
        target_grid_lines_count_x = canvas_width // cell_width
        target_grid_lines_count_y = canvas_height // cell_height
            

        
        for column in range(target_grid_lines_count_x):
            
            line_color = "gray"
            line_width = 1
            
            if (column + 1) % width_in_cells == 0:
                line_width = 2
                line_color = "black"
                
            self.canvas.create_line(
                (column + 1) * cell_width,
                0,
                (column + 1) * cell_width,
                canvas_height,
                fill = line_color,
                width = line_width
            )
    
        for row in range(target_grid_lines_count_y):
            
            line_color = "gray"
            line_width = 1
            
            if (row + 1) % height_in_cells == 0:
                line_width = 2
                line_color = "black"
                
            self.canvas.create_line(
                0,
                (row + 1) * cell_height,
                canvas_width,
                (row + 1) * cell_height,
                fill = line_color,
                width = line_width
            )
            
        
class Query(tkSimpleDialog.Dialog):

    def body(self, master):

        self.e1 = tk.Entry(master)
        self.e1.pack()

        return self.e1 # initial focus

    def apply(self): 
        self.result = self.e1.get()
        

        

        