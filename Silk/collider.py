from list import *
from physics_system import *
import numpy as np
from rigid_body import *
import unittest
from collision_space import *
from shape import *
#mutual dependent interface ColliderMover
#TODO change list to container or set

class Collider: #Containable
    
    def __init__(self, rigid_body, shape):
        
        self.rigid_body = rigid_body 
        self.shape = shape 
        self.position = np.array([0,0])
        self.hard_surjective_set = Smart_List()
        self.soft_surjective_set = Smart_List()
        self.injective_set = Smart_List() 
        
        self.contained_by_set = Smart_Cross_List()
        
        
    def join(self, collision_space):
        if collision_space in self.injective_set:
            raise ValueError(
                "Collider can not join a collision space more than once"
            )
        collider_position = self.get_position()
        node = collision_space.get_cell_at_position(collider_position).add(self)
        self.injective_set.add(Entry(collision_space,node))
        return node #to leave a collision_space, call .empty() on this node
    
    def update_injectives(self):
        
        collider_position = self.get_position()
        for entry in self.injective_set:
            node = entry.get_value()
            collision_space = entry.get_key()
            node.eject()
            insert_after(
                node,
                collision_space.get_cell_at_position(collider_position)
            )
            
    def hard_watch(self, collision_space):
        if collision_space in self.hard_surjective_set:
            raise ValueError(
                "Collider can not hard watch a collision space more than once"
            )
        node = self.hard_surjective_set.add(collision_space)
        return node
        
    def soft_watch(self, collisiont_space):
        if collision_space in self.soft_surjective_set:
            raise ValueError(
                "Collider can not soft watch a collision space more than once"
            )
        node = self.soft_surjective_set.add(collision_space)
        return node
        
    def get_shape(self):
        return self.shape
        
    def get_position(self):
        return self.shape.get_position(
            self.rigid_body.get_position(),
            self.rigid_body.get_orientation()
        )
        
    def get_orientation(self):
        return self.rigid_body.get_orientation()
    
    def get_contained_by_set(self):
        return self.contained_by_set
        
    def get_bounds(self):
        return self.shape.get_bounds(
            self.rigid_body.get_position(),
            self.rigid_body.get_orientation()
        )
        
    def empty(self):
        self.rigid_body = None
        self.position = None
        self.shape = None
        self.hard_surjective_set = self.hard_surjective_set.empty()
        self.soft_surjective_set = self.soft_surjective_set.empty()
        self.injective_set = self.injective_set.empty()
        
        self.contained_by_set = self.contained_by_set.cross_empty()
        
        return None


class Collider_Test(unittest.TestCase):
    
    def test_get_position(self):
        collider = Collider(Rigid_Body(np.array([3, 4])), Point(np.array([5, 9])))
        self.assertEqual(collider.get_position()[0], 8)
        self.assertEqual(collider.get_position()[1], 13)
        collider = Collider(Rigid_Body(np.array([3, 4])), Point(np.array([-5, -9])))
        self.assertEqual(collider.get_position()[0], -2)
        self.assertEqual(collider.get_position()[1], -5)
        
    def test_join(self):
        collision_space1 = Collision_Space(30,30,10,10)
        collision_space2 = Collision_Space(50,50,10,10)
        collision_space3 = Collision_Space(30,30,20,20)
        collision_space4 = Collision_Space(1,1,1,1)
        collider1 = Collider(Rigid_Body(np.array([3, 4])), Point(np.array([5, 9])))
        collider1.join(collision_space1)
        collider1.join(collision_space2)
        collider1.join(collision_space3)
        collider1.join(collision_space4)
        self.assertIn(collider1, collision_space1.get_hash_grid()[0][0])
        self.assertIn(collider1, collision_space2.get_hash_grid()[0][0])
        self.assertIn(collider1, collision_space3.get_hash_grid()[0][0])
        self.assertIn(collider1, collision_space4.get_hash_grid()[0][0])
        collider2 = Collider(Rigid_Body(np.array([0, 0])), Point(np.array([-1, -1])))
        collider2.join(collision_space1)
        collider2.join(collision_space2)
        collider2.join(collision_space3)
        collider2.join(collision_space4)
        self.assertIn(collider2, collision_space1.get_hash_grid()[9][9])
        self.assertIn(collider2, collision_space2.get_hash_grid()[9][9])
        self.assertIn(collider2, collision_space3.get_hash_grid()[19][19])
        self.assertIn(collider2, collision_space4.get_hash_grid()[0][0])
        collider3 = Collider(Rigid_Body(np.array([0, 0])), Point(np.array([-49, -49])))
        collider3.join(collision_space1)
        collider3.join(collision_space2)
        collider3.join(collision_space3)
        collider3.join(collision_space4)
        self.assertIn(collider3, collision_space1.get_hash_grid()[8][8])
        self.assertIn(collider3, collision_space2.get_hash_grid()[9][9])
        self.assertIn(collider3, collision_space3.get_hash_grid()[18][18])
        self.assertIn(collider3, collision_space4.get_hash_grid()[0][0])
        collider4 = Collider(Rigid_Body(np.array([0, 0])), Point(np.array([589, 589])))
        collider4.join(collision_space1)
        collider4.join(collision_space2)
        collider4.join(collision_space3)
        collider4.join(collision_space4)
        self.assertIn(collider4, collision_space1.get_hash_grid()[9][9])
        self.assertIn(collider4, collision_space2.get_hash_grid()[1][1])
        self.assertIn(collider4, collision_space3.get_hash_grid()[19][19])
        self.assertIn(collider4, collision_space4.get_hash_grid()[0][0])
        
        # Test Removal
        collider1.empty()
        collider2.empty()
        collider3.empty()
        #collider4 is not deleted 
        self.assertNotIn(collider1, collision_space1.get_hash_grid()[0][0])
        self.assertNotIn(collider1, collision_space2.get_hash_grid()[0][0])
        self.assertNotIn(collider1, collision_space3.get_hash_grid()[0][0])
        self.assertNotIn(collider1, collision_space4.get_hash_grid()[0][0])
        self.assertNotIn(collider2, collision_space1.get_hash_grid()[9][9])
        self.assertNotIn(collider2, collision_space2.get_hash_grid()[9][9])
        self.assertNotIn(collider2, collision_space3.get_hash_grid()[19][19])
        self.assertNotIn(collider2, collision_space4.get_hash_grid()[0][0])
        self.assertNotIn(collider3, collision_space1.get_hash_grid()[8][8])
        self.assertNotIn(collider3, collision_space2.get_hash_grid()[9][9])
        self.assertNotIn(collider3, collision_space3.get_hash_grid()[18][18])
        self.assertNotIn(collider3, collision_space4.get_hash_grid()[0][0])
        self.assertIn(collider4, collision_space1.get_hash_grid()[9][9])
        self.assertIn(collider4, collision_space2.get_hash_grid()[1][1])
        self.assertIn(collider4, collision_space3.get_hash_grid()[19][19])
        self.assertIn(collider4, collision_space4.get_hash_grid()[0][0])
        self.assertEqual(len(list(collider4.injective_set)), 4)

        for entry in collider4.injective_set:
            node = entry.get_value()
            node.eject()
            entry.empty()
    
        self.assertEqual(len(list(collider4.injective_set)), 0)
        self.assertNotIn(collider4, collision_space1.get_hash_grid()[9][9])
        self.assertNotIn(collider4, collision_space2.get_hash_grid()[1][1])
        self.assertNotIn(collider4, collision_space3.get_hash_grid()[19][19])
        self.assertNotIn(collider4, collision_space4.get_hash_grid()[0][0])
        
    def test_update_injectives(self):
        collision_space1 = Collision_Space(30,30,10,10)
        collision_space2 = Collision_Space(50,50,10,10)
        collision_space3 = Collision_Space(30,30,20,20)
        collision_space4 = Collision_Space(1,1,1,1)
        location  = np.array([5, 9])
        collider = Collider(Rigid_Body(np.array([0, 0])), Point(location))
        collider.join(collision_space1)
        collider.join(collision_space2)
        collider.join(collision_space3)
        collider.join(collision_space4)
        collider.update_injectives()
        self.assertIn(collider, collision_space1.get_hash_grid()[0][0])
        self.assertIn(collider, collision_space2.get_hash_grid()[0][0])
        self.assertIn(collider, collision_space3.get_hash_grid()[0][0])
        self.assertIn(collider, collision_space4.get_hash_grid()[0][0])
        location[0] = -1
        location[1] = -1
        collider.update_injectives()
        self.assertIn(collider, collision_space1.get_hash_grid()[9][9])
        self.assertIn(collider, collision_space2.get_hash_grid()[9][9])
        self.assertIn(collider, collision_space3.get_hash_grid()[19][19])
        self.assertIn(collider, collision_space4.get_hash_grid()[0][0])
        self.assertNotIn(collider, collision_space1.get_hash_grid()[0][0])
        self.assertNotIn(collider, collision_space2.get_hash_grid()[0][0])
        self.assertNotIn(collider, collision_space3.get_hash_grid()[0][0])
        location[0] = -49
        location[1] = -49
        collider.update_injectives()
        self.assertIn(collider, collision_space1.get_hash_grid()[8][8])
        self.assertIn(collider, collision_space2.get_hash_grid()[9][9])
        self.assertIn(collider, collision_space3.get_hash_grid()[18][18])
        self.assertIn(collider, collision_space4.get_hash_grid()[0][0])
        self.assertNotIn(collider, collision_space1.get_hash_grid()[9][9])
        self.assertNotIn(collider, collision_space3.get_hash_grid()[19][19])
        location[0] = 589
        location[1] = 589
        collider.update_injectives()
        self.assertIn(collider, collision_space1.get_hash_grid()[9][9])
        self.assertIn(collider, collision_space2.get_hash_grid()[1][1])
        self.assertIn(collider, collision_space3.get_hash_grid()[19][19])
        self.assertIn(collider, collision_space4.get_hash_grid()[0][0])
        self.assertNotIn(collider, collision_space1.get_hash_grid()[8][8])
        self.assertNotIn(collider, collision_space2.get_hash_grid()[9][9])
        self.assertNotIn(collider, collision_space3.get_hash_grid()[18][18])
    
    def test_get_bounds(self):
        collider = Collider(Rigid_Body(np.array([0, 0])), Point(np.array([-1, -1])))
        self.assertEqual(collider.get_bounds().get_left(), -1)
        self.assertEqual(collider.get_bounds().get_top(), -1)
        
        collider = Collider(Rigid_Body(np.array([0, 0])), Rectangle(1, 1, 1, 1))
        self.assertEqual(collider.get_bounds().get_left(), -1)
        self.assertEqual(collider.get_bounds().get_top(), -1)
        self.assertEqual(collider.get_bounds().get_width(), 2)
        self.assertEqual(collider.get_bounds().get_height(), 2)
        
        collider = Collider(Rigid_Body(np.array([1, 1])), Rectangle(1, 1, 1, 1))
        self.assertEqual(collider.get_bounds().get_left(), 0)
        self.assertEqual(collider.get_bounds().get_top(), 0)
        self.assertEqual(collider.get_bounds().get_width(), 2)
        self.assertEqual(collider.get_bounds().get_height(), 2)
        
        
collider_test_suite = unittest.TestLoader().loadTestsFromTestCase(Collider_Test)


