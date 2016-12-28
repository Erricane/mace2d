"""
Connectable
next (Get and Set)
previous (Get and Set)
"""

"""
Cross_Connectable
cross_next (Get and Set)
cross_previous (Get and Set)
"""

"""
Containable
get_contained_by_set()
empty() must be used in assignment like: x = x.empty() [returns None]
"""
import unittest


class Smart_List: #Connectable
    
    def __init__(self):
        self.next = None
        self.previous = None
        
    def __iter__(self):
        return Smart_List_Iterator(self)
        
    def __repr__(self):
        return str(list(self))
    
    def add (self, obj):
        self.next = Node(obj, self)
        return self.next
        
    def add_node(self,node):
        connect(node,self.get_next())
        connect(self,node)
        
    def empty(self):
        for connectable in Smart_List_Connectable_Iterator(self):
            connectable.empty()
        self.next = None
        self.previous = None
        return None
        
    def get_next(self):
        return self.next
        
    def set_next(self, connectable):
        self.next = connectable
        
    def set_previous(self, connectable):
        pass
        
    def get_previous(self):
        return None
            
def Smart_List_Iterator(connectable):
    
    position = connectable
    next_position = connectable.get_next()
    
    while next_position != None:
        position = next_position
        next_position = position.get_next()
        yield position.get_containable()
        
        
def Smart_List_Connectable_Iterator(connectable):
    
    position = connectable
    next_position = connectable.get_next()
    
    while next_position != None:
        position = next_position
        next_position = position.get_next()
        yield position
        

class Smart_Cross_List: #Cross_Connectable
    
    def __init__(self):
        self.cross_next = None
        self.cross_previous = None
        
    def __iter__(self):
        return Smart_Cross_List_Iterator(self)
        
    def cross_empty(self):
        for cross_connectable in self:
            cross_connectable.cross_empty()
        self.cross_next = None
        self.cross_previous = None
        return None
        
    def get_cross_next(self):
        return self.cross_next
        
    def set_cross_next(self, cross_connectable):
        self.cross_next = cross_connectable
        
    def set_cross_previous(self, cross_connectable):
        pass
        
    def get_cross_previous(self):
        return None
    
        
def Smart_Cross_List_Iterator(cross_connectable):
    
    position = cross_connectable
    next_position = cross_connectable.get_cross_next()
    
    while next_position != None:
        position = next_position
        next_position = position.get_cross_next() 
        yield position
           
            
class Node: #Connectable, Cross_Connectable
    
    def __init__(self, containable, connectable = None):
        
        self.containable = containable
        self.next = None
        self.previous = None
        self.cross_next = None
        self.cross_previous = None
        
        insert_after(self, connectable)
        cross_insert_after(self, containable.get_contained_by_set())
        
        self.contained_by_set = Smart_Cross_List()

    def get_contained_by_set(self):
        return self.contained_by_set
        
    def eject(self):
        connect(self.previous, self.next)
        self.previous = None
        self.next = None
        
    def empty(self):
        connect(self.previous, self.next)
        cross_connect(self.cross_previous, self.cross_next)
        self.containable = None
        self.next = None
        self.previous = None
        self.cross_next = None
        self.cross_previous = None
        self.contained_by_set = self.contained_by_set.cross_empty()
        return None
        
    def cross_empty(self):
        return self.empty()
        
    def set_next(self,connectable):
        self.next = connectable
    
    def get_next(self):
        return self.next
        
    def set_previous(self,connectable):
        self.previous = connectable
        
    def get_previous(self):
        return self.previous
        
    def set_cross_next(self,cross_connectable):
        self.cross_next = cross_connectable
    
    def get_cross_next(self):
        return self.cross_next
        
    def set_cross_previous(self,cross_connectable):
        self.cross_previous = cross_connectable
        
    def get_cross_previous(self):
        return self.cross_previous
        
    def get_containable(self):
        return self.containable
        
class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.contained_by_set = Smart_Cross_List()
        
    def __repr__(self):
        return "{" + str(self.key) + ": " + str(self.value) + "}"
    
    def get_key(self):
        return self.key
        
    def get_value(self):
        return self.value
        
    def get_contained_by_set(self):
        return self.contained_by_set
        
    def empty(self):
        self.contained_by_set = self.contained_by_set.cross_empty()
        self.key = None
        self.value = None
        return None
        
class Item:
    def __init__(self, value):
        self.value = value
        self.contained_by_set = Smart_Cross_List()
        
    def __repr__(self):
        return str(self.value)
        
    def get_value(self):
        return self.value
        
    def get_contained_by_set(self):
        return self.contained_by_set
        
    def empty(self):
        self.contained_by_set = self.contained_by_set.cross_empty()
        self.value = None
        return None
        
def connect(previous_node, next_node):
    if previous_node != None:
        previous_node.set_next(next_node)
    if next_node != None:
        next_node.set_previous(previous_node)
        
def insert_after(inserted, connectable):
        if connectable != None:
            connect(inserted,connectable.get_next())
            connect(connectable,inserted)
        
def cross_connect(previous_node, next_node):
    if previous_node != None:
        previous_node.set_cross_next(next_node)
    if next_node != None:
        next_node.set_cross_previous(previous_node)
        
def cross_insert_after(inserted, cross_connectable):
        cross_connect(inserted ,cross_connectable.get_cross_next())
        cross_connect(cross_connectable, inserted)
        
        
class List_Test(unittest.TestCase):
    def test_list(self):
        smart_list = Smart_List()
        smart_list.add(Item(5))
        smart_list.add(Item(10))
        smart_list.add(Item(15))
        
        node_list = list(Smart_List_Connectable_Iterator(smart_list))
        
        self.assertEqual(node_list[0].get_containable().get_value(), 15)
        self.assertEqual(node_list[1].get_containable().get_value(), 10)
        self.assertEqual(node_list[2].get_containable().get_value(), 5)
        
        item_list = list(smart_list)
        
        node_list = list(Smart_List_Connectable_Iterator(smart_list))
        
        self.assertEqual(item_list[0].get_value(), 15)
        self.assertEqual(item_list[1].get_value(), 10)
        self.assertEqual(item_list[2].get_value(), 5)
        
        new_node = Node(Item(20))
        smart_list.add_node(new_node)
        item_list = list(smart_list)
        
        self.assertEqual(item_list[0].get_value(), 20)
        self.assertEqual(item_list[1].get_value(), 15)
        self.assertEqual(item_list[2].get_value(), 10)
        self.assertEqual(item_list[3].get_value(), 5)
        
        for item in item_list[0:2]:
            item.empty()
            
        item_list = list(smart_list)
        self.assertEqual(item_list[0].get_value(), 10)
        self.assertEqual(item_list[1].get_value(), 5)
        
        smart_list.add(Item(5))
        smart_list.add(Item(10))
        smart_list.add(Item(15))
        
        test_list = [15, 10, 5, 10, 5]
        for item in smart_list:
            self.assertEqual(item.get_value(), test_list.pop(0))
            item.empty()
            
if __name__ == "__main__":            
    list_test_suite = unittest.TestLoader().loadTestsFromTestCase(List_Test)
           
        
        
