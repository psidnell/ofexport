import unittest
from typeof import TypeOf

class Parent(object):
    pass

class Child (Parent):
    pass

class DemoClass(object):
    string = TypeOf ("string", str)
    child = TypeOf ("child", Child)
    parent = TypeOf ("parent", Parent)

class Test_typeof(unittest.TestCase):
    
    def test_field_access_when_not_set (self):
        demo = DemoClass ()
        self.assertEqual (None, demo.string)
        
    def test_field_access_when_set (self):
        demo = DemoClass ()
        demo.string = 'xxx'
        self.assertEqual ('xxx', demo.string)
        
    def test_set_to_null (self):
        demo = DemoClass ()
        demo.string = None
        self.assertEqual (None, demo.string)
        
    def test_set_to_bad_type (self):
        demo = DemoClass ()
        try:
            demo.string = 42
            self.fail('expected error')
        except AssertionError as e:
            self.assertEqual("string: expected type <type 'str'> got <type 'int'>", e.message)
            
    def test_type_hierarchy_ok (self):
        demo = DemoClass ()
        demo.child = Child ()
        demo.parent = Parent ()
        demo.parent = Child ()
       
    def test_type_hierarchy_bad (self):
        demo = DemoClass ()
        try:
            demo.child = Parent ()
            self.fail('expected error')
        except AssertionError as e:
            self.assertEqual("child: expected type <class 'types_test.Child'> got <class 'types_test.Parent'>", e.message)
        