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

from cmd_parser import tokenise

def pretty_tokens (tokens):
    result = []
    for typ, val in tokens:
        if typ == 'TXT':
            result.append ('"' + val + '"')
        else:
            result.append (typ)
    return ','.join(result)
    
class Test_cmd_parser(unittest.TestCase):
    
    def test_tokenisation(self):
        self.assertEquals('"aa",OB,"bb",CB,"cc"', pretty_tokens(tokenise ('aa(bb)cc')))
        self.assertEquals('"aa",DQ,"bb",DQ,"cc",EQ', pretty_tokens(tokenise ('aa"bb"cc=')))
        self.assertEquals('"aa",SQ,"bb",SQ,"cc",EQ', pretty_tokens(tokenise ("aa'bb'cc=")))
        self.assertEquals('"a ",NE," b"', pretty_tokens(tokenise ("a != b")))
        self.assertEquals('"a ",AND," b"', pretty_tokens(tokenise ("a and b")))
        self.assertEquals('"a ",OR," b"', pretty_tokens(tokenise ("a or b")))
        self.assertEquals('NOT," a"', pretty_tokens(tokenise ("not a")))
        self.assertEquals('"ab",BS,"cd"', pretty_tokens(tokenise ("ab\\cd")))
        self.assertEquals('"a",""","b"', pretty_tokens(tokenise ('a\\"b')))
        self.assertEquals('"a","\'","b"', pretty_tokens(tokenise ("a\\'b")))


        
