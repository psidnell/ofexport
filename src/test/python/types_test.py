'''
Copyright 2013 Paul Sidnell

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

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
        