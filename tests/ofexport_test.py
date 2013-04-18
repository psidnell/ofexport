import unittest

from ofexport import parse_command

class Test_ofexport(unittest.TestCase):
    
    def test_parse_command (self):
        included, field, arg = parse_command ("name=xyz")
        self.assertEquals (True, included)
        self.assertEquals ("name", field)
        self.assertEquals ("xyz", arg)
        
        included, field, arg = parse_command ("name!=xyz")
        self.assertEquals (False, included)
        self.assertEquals ("name", field)
        self.assertEquals ("xyz", arg)
        
        included, field, arg = parse_command ("flagged")
        self.assertEquals (True, included)
        self.assertEquals ("flagged", field)
        self.assertEquals (None, arg)
        
        included, field, arg = parse_command ("!flagged")
        self.assertEquals (False, included)
        self.assertEquals ("flagged", field)
        self.assertEquals (None, arg)

        included, field, arg = parse_command ("!=xyz")
        self.assertEquals (False, included)
        self.assertEquals ("", field)
        self.assertEquals ("xyz", arg)
        
        included, field, arg = parse_command ("=xyz")
        self.assertEquals (True, included)
        self.assertEquals ("", field)
        self.assertEquals ("xyz", arg)
        
        included, field, arg = parse_command ("name!=")
        self.assertEquals (False, included)
        self.assertEquals ("name", field)
        self.assertEquals ("", arg)
        
        included, field, arg = parse_command ("name=")
        self.assertEquals (True, included)
        self.assertEquals ("name", field)
        self.assertEquals ("", arg)