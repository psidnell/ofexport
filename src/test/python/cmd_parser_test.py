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
from datetime import datetime
from treemodel import Task
from cmd_parser import tokenise, consume_whitespace, parse_string, parse_expr, ALIAS_LOOKUPS
from datematch import date_range_to_str

def pretty_tokens (tokens):
    result = []
    for typ, val in tokens:
        if typ == 'TXT':
            result.append ('"' + val + '"')
        else:
            result.append (typ)
    return ','.join(result)
    
class Test_cmd_parser(unittest.TestCase):
    
    def test_alias_lookup (self):
        self.assertEquals ('date_due', ALIAS_LOOKUPS['due'])
        self.assertEquals ('flagged', ALIAS_LOOKUPS['flagged'])
    
    def test_tokenisation(self):
        self.assertEquals('"aa",OB,"bb",CB,"cc"', pretty_tokens(tokenise ('aa(bb)cc')))
        self.assertEquals('"aa",DQ,"bb",DQ,"cc",EQ', pretty_tokens(tokenise ('aa"bb"cc=')))
        self.assertEquals('"a",SP,NE,SP,"b"', pretty_tokens(tokenise ("a != b")))
        self.assertEquals('"a",SP,AND,SP,"b"', pretty_tokens(tokenise ("a and b")))
        self.assertEquals('"a",SP,OR,SP,"b"', pretty_tokens(tokenise ("a or b")))
        self.assertEquals('NOT,SP,"a"', pretty_tokens(tokenise ("! a")))
        self.assertEquals('"ab",BS,"cd"', pretty_tokens(tokenise ("ab\\cd")))
        self.assertEquals('"a",""","b"', pretty_tokens(tokenise ('a\\"b')))

    def test_consume_whitespace (self):
        self.assertEquals('"x"', pretty_tokens (consume_whitespace ([('SP', ' '),('SP', ' '),('SP', ' '),('TXT','x')])))
        self.assertEquals('"x"', pretty_tokens (consume_whitespace ([('SP', ' '),('SP', ' '),('TXT','x')])))
        self.assertEquals('"x"', pretty_tokens (consume_whitespace ([('SP', ' '),('TXT','x')])))
        self.assertEquals('"x"', pretty_tokens (consume_whitespace ([('TXT','x')])))
        self.assertEquals('', pretty_tokens (consume_whitespace ([])))
        
    def test_parse_string (self):
        string, tokens = parse_string ([('SP', ' '),('TXT','x'),('TXT','y'),('CB', ')')], 'CB')
        self.assertEquals('xy', string)
        self.assertEquals('CB', pretty_tokens (tokens))
        
        string, tokens = parse_string ([('SP', ' '),('TXT','x'),('TXT','y')], 'CB')
        self.assertEquals('xy', string)
        self.assertEquals('', pretty_tokens (tokens))
    
    def test_parse_expr_true (self):
        expr  = parse_expr(tokenise ('true'))[0]
        self.assertTrue(expr (None))
    
    def test_parse_expr_false (self):
        expr = parse_expr(tokenise ('false'))[0]
        self.assertFalse(expr (None))
  
    def test_parse_expr_not (self):
        expr = parse_expr(tokenise ('!true'))[0]
        self.assertFalse(expr (None))
        
        expr = parse_expr(tokenise ('!(true)'))[0]
        self.assertFalse(expr (None))
        
        expr = parse_expr(tokenise ('(!(true))'))[0]
        self.assertFalse(expr (None))
    
    def test_parse_expr_and (self):
        expr = parse_expr(tokenise ('true and true'))[0]
        self.assertTrue(expr (None))

        expr = parse_expr(tokenise ('true and false'))[0]
        self.assertFalse(expr (None))

        expr = parse_expr(tokenise ('false and true'))[0]
        self.assertFalse(expr (None))
        
        expr = parse_expr(tokenise ('false and false'))[0]
        self.assertFalse(expr (None))

    def test_parse_expr_or (self):
        expr = parse_expr(tokenise ('true or true'))[0]
        self.assertTrue(expr (None))

        expr = parse_expr(tokenise ('true or false'))[0]
        self.assertTrue(expr (None))

        expr = parse_expr(tokenise ('false or true'))[0]
        self.assertTrue(expr (None))
        
        expr = parse_expr(tokenise ('false or false'))[0]
        self.assertFalse(expr (None))
        
    def test_parse_expr_equals (self):
        expr = parse_expr(tokenise ('true = true'))[0]
        self.assertTrue(expr (None))

        expr = parse_expr(tokenise ('true = false'))[0]
        self.assertFalse(expr (None))

        expr = parse_expr(tokenise ('false = true'))[0]
        self.assertFalse(expr (None))
        
        expr = parse_expr(tokenise ('false = false'))[0]
        self.assertTrue(expr (None))
        
    def test_parse_expr_string (self):
        expr = parse_expr(tokenise ('"xxx" = "xxx"'))[0]
        self.assertTrue(expr (None))
        expr = parse_expr(tokenise ('"xxx" = "yyy"'))[0]
        self.assertFalse(expr (None))

        
    def test_parse_expr_not_equals (self):
        expr = parse_expr(tokenise ('true != true'))[0]
        self.assertFalse(expr (None))

        expr = parse_expr(tokenise ('true != false'))[0]
        self.assertTrue(expr (None))

        expr = parse_expr(tokenise ('false != true'))[0]
        self.assertTrue(expr (None))
        
        expr = parse_expr(tokenise ('false != false'))[0]
        self.assertFalse(expr (None))
        
    def test_parse_expr_flagged (self):
        expr = parse_expr(tokenise ('flagged'))[0]
        self.assertTrue(expr (Task(flagged=True)))
        self.assertFalse(expr (Task(flagged=False)))
        
        expr = parse_expr(tokenise ('flagged = true'))[0]
        self.assertTrue(expr (Task(flagged=True)))
        self.assertFalse(expr (Task(flagged=False)))
        
        expr = parse_expr(tokenise ('true = flagged'))[0]
        self.assertTrue(expr (Task(flagged=True)))
        self.assertFalse(expr (Task(flagged=False)))
        
        expr = parse_expr(tokenise ('!flagged'))[0]
        self.assertFalse(expr (Task(flagged=True)))
        self.assertTrue(expr (Task(flagged=False)))
        
    def test_parse_expr_brackets (self):
        expr = parse_expr(tokenise ('(true)'))[0]
        self.assertTrue(expr (None))
        expr  = parse_expr(tokenise ('(false)'))[0]
        self.assertFalse(expr (None))
        expr  = parse_expr(tokenise (' ( false ) '))[0]
        self.assertFalse(expr (None))
        expr = parse_expr(tokenise ('(false or true)'))[0]
        self.assertTrue(expr (None))
        expr = parse_expr(tokenise ('(false) or (true)'))[0]
        self.assertTrue(expr (None))
        expr = parse_expr(tokenise ('((false) or (true))'))[0]
        self.assertTrue(expr (None))
        
    def test_parse_expr_date(self):
        tue = datetime.strptime('Apr 9 2013 11:33PM', '%b %d %Y %I:%M%p')
        expr = parse_expr(tokenise ('[today]'), now=tue)[0]
        self.assertEquals ("2013-04-09", date_range_to_str (expr(None)))
        expr = parse_expr(tokenise ('[last tues]'), now=tue)[0]
        self.assertEquals ("2013-04-02", date_range_to_str (expr(None)))
        expr = parse_expr(tokenise ('due = [today]'), now=tue)[0]
        self.assertTrue (expr(Task(name="", date_due=tue)))
        
        