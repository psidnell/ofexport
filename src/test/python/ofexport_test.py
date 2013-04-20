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