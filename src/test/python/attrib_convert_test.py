import unittest

from treemodel import Task
from attrib_convert import Conversion, AttribMapBuilder

class Test_conversion_convert(unittest.TestCase):
    
    def test_convert_attribute (self):
        type_fns = {}
        type_fns['string'] = lambda x: x
        
        conversion = Conversion ("nosuchconversion", "default value", "($value)", "string")
        self.assertEquals("default value", conversion.value(Task (), type_fns))
        
        conversion = Conversion ("name", "default value", "($value)", "string")
        self.assertEquals("default value", conversion.value(Task (), type_fns))
        
        conversion = Conversion ("name", "default value", "($value)", "string")
        self.assertEquals("(123)", conversion.value(Task (name="123"), type_fns))
        
    def test_build_attribute_map (self):
        builder = AttribMapBuilder ()
        values = builder.get_values(Task (name="123"))
        self.assertEqual("123", values["name"])
    