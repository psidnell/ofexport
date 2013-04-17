import unittest

from ofexport import parse_command

class Test_ofexport(unittest.TestCase):
    
    def test_parse_command (self):
        instruction, field, arg = parse_command ("include:name:x:y:z")
        self.assertEquals ("include", instruction)
        self.assertEquals ("name", field)
        self.assertEquals ("x:y:z", arg)
        
        instruction, field, arg = parse_command ("exclude:name:x:y:z")
        self.assertEquals ("exclude", instruction)
        self.assertEquals ("name", field)
        self.assertEquals ("x:y:z", arg)
        
        instruction, field, arg = parse_command ("sort:name")
        self.assertEquals ("sort", instruction)
        self.assertEquals ("name", field)
        self.assertEquals (None, arg)
        
        instruction, field, arg = parse_command ("exclude:flagged")
        self.assertEquals ("exclude", instruction)
        self.assertEquals ("flagged", field)
        self.assertEquals (None, arg)
