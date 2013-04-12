import unittest
from util import strip_tabs_newlines

class Test_util(unittest.TestCase):
    
    def test_strip_tabs_newlines (self):
        self.assertEquals ('aa bb cc dd ee', strip_tabs_newlines (' aa\nbb cc\ndd\tee'))