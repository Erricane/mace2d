from list import *
from bounds import *

#TODO make collision space continuous in select spaces only

class Collision_Space: #Containable | is a generic of template Collider
    def __init__(self, cell_width, cell_height, width_in_cells, height_in_cells):
        
        self.width_in_cells = width_in_cells
        self.height_in_cells = height_in_cells
        self.cell_width = cell_width
        self.cell_height = cell_height
        
        self.hash_grid = [[Smart_List() for y in range(height_in_cells)] 
            for x in range(width_in_cells)]
            
        self.contained_by_list = Smart_Cross_List()
            
        
    def get_cell_at_position(self,position):
        return(
            self.hash_grid
                [self.get_hash_position_x(position)]
                [self.get_hash_position_y(position)]
        )
                                             
                                             
    def get_hash_position_x(self,position):
        return hash_position(
                    position[0], 
                    self.width_in_cells, 
                    self.cell_width
               )
        
    def get_hash_position_y(self,position):
        return hash_position(
                    position[1], 
                    self.height_in_cells, 
                    self.cell_height
               )
        
    def get_hash_remainder_x(self,position):
        return hash_remainder(position[0], self.cell_width)
        
    def get_hash_remainder_y(self,position):
        return hash_remainder(position[1], self.cell_height)

    def move_collider(self, node):
        #take the node out of the list and add it back into the hash_grid
        pass
        
    def get_hash_grid(self):
        return self.hash_grid
        
    def get_contained_by_list(self):
        return self.contained_by_list
    
    def empty(self):
        return None
        
    def Collision_Space_Iterator(self,bounds):
        search_origin = bounds.get_origin()
        x_range = bounds.get_width()
        y_range = bounds.get_height()
        
        start_x = ((self.get_hash_position_x(search_origin) - 1) %
                    self.width_in_cells)
        start_y = ((self.get_hash_position_y(search_origin) - 1) %
                    self.height_in_cells)
        
        search_width =  min(int((self.get_hash_remainder_x(search_origin) +
                                x_range) // self.cell_width) + 3, 
                            self.width_in_cells)
                            
        search_height = min(int((self.get_hash_remainder_y(search_origin) +                 
                                y_range) // self.cell_height) + 3, 
                            self.height_in_cells)
                                
        x_index = start_x 
        
                                
        for i in range(search_width):
            y_index = start_y 
            
            for j in range(search_height):
                for other in self.hash_grid[x_index][y_index]:
                    
                    yield other
                y_index = (y_index + 1) % self.height_in_cells
            x_index = (x_index + 1) % self.width_in_cells
            
    def Collision_Space_Index_Iterator(self,bounds):
        search_origin = bounds.get_origin()
        x_range = bounds.get_width()
        y_range = bounds.get_height()
        
        start_x = self.get_hash_position_x(search_origin)
        start_y = self.get_hash_position_y(search_origin)
        
        start_x = ((self.get_hash_position_x(search_origin) - 1) %
                    self.width_in_cells)
        start_y = ((self.get_hash_position_y(search_origin) - 1) %
                    self.height_in_cells)
        
        search_width =  min(int((self.get_hash_remainder_x(search_origin) +
                                x_range) // self.cell_width) + 3, 
                            self.width_in_cells)
                            
        search_height = min(int((self.get_hash_remainder_y(search_origin) +                 
                                y_range) // self.cell_height) + 3, 
                            self.height_in_cells)
                                
        x_index = start_x 
        
                                
        for i in range(search_width):
            y_index = start_y 
            
            for j in range(search_height):
                yield x_index, y_index
                y_index = (y_index + 1) % self.height_in_cells
            x_index = (x_index + 1) % self.width_in_cells
        
    def get_cell_width(self):
        return self.cell_width
    
    def get_cell_height(self):
        return self.cell_height
        
    def get_width_in_cells(self):
        return self.width_in_cells
        
    def get_height_in_cells(self):
        return self.height_in_cells
        
        
#always use positive modulus
def hash_position(position,cell_count,cell_width):
    cell_position = position // cell_width
    hashed_cell_position = cell_position % cell_count
    return hashed_cell_position
    
def hash_remainder(position,cell_width):
    return position % cell_width
    

    

