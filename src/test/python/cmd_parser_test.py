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
from treemodel import Task, Project, Folder
from cmd_parser import DATE_TYPE, STRING_TYPE, Note, tokenise, read_to_end_quote, parse_string, parse_expr, make_command_filter, make_expr_filter, ALIAS_LOOKUPS
from datematch import date_range_to_str
from visitors import Sort, Prune, Flatten, Filter
from test_helper import catch_exception

class TestNote (Note):
    def __init__ (self, text):
        self.text = text
        self.lines = text.split('\n')
    def get_note (self):
        return self.text
    def get_note_lines (self):
        return self.lines

def pretty_tokens (tokens):
    result = []
    for typ, val in tokens:
        if typ == 'TXT':
            result.append (val)
        elif typ == 'QTXT':
            result.append ('"' + val + '"')
        else:
            result.append (typ)
    return ','.join(result)
    
class Test_cmd_parser(unittest.TestCase):
    
    def test_alias_lookup (self):
        self.assertEquals ('date_due', ALIAS_LOOKUPS['due'])
        self.assertEquals ('flagged', ALIAS_LOOKUPS['flagged'])
    
    def test_read_to_end_quote (self):
        string, remainder = read_to_end_quote ('"', '"')
        self.assertEquals('', string)
        self.assertEquals ('', remainder)
        
        string, remainder = read_to_end_quote ('"', 'a"')
        self.assertEquals('a', string)
        self.assertEquals ('', remainder)
        
        string, remainder = read_to_end_quote ('"', 'abc"')
        self.assertEquals('abc', string)
        self.assertEquals ('', remainder)
        
        string, remainder = read_to_end_quote ('"', 'abc"stuff')
        self.assertEquals('abc', string)
        self.assertEquals ('stuff', remainder)
        
        string, remainder = read_to_end_quote ('"', 'abc"stuff')
        self.assertEquals('abc', string)
        self.assertEquals ('stuff', remainder)
        
        string, remainder = read_to_end_quote ('"', 'abc\\"def"stuff')
        self.assertEquals('abc"def', string)
        self.assertEquals ('stuff', remainder)  
        
        string, remainder = read_to_end_quote ('"', 'abc\\def"stuff')
        self.assertEquals('abc\\def', string)
        self.assertEquals ('stuff', remainder)
        
        string, remainder = read_to_end_quote ('"', 'abc\\\\def"stuff')
        self.assertEquals('abc\\def', string)
        self.assertEquals ('stuff', remainder)  
        
    def test_tokenisation(self):
        self.assertEquals('aa,OB,bb,CB,cc', pretty_tokens(tokenise ('aa(bb)cc')))
        self.assertEquals('aa,"bb",cc,EQ', pretty_tokens(tokenise ('aa"bb"cc=')))
        self.assertEquals('aa,"bb",cc,EQ', pretty_tokens(tokenise ("aa'bb'cc=")))
        self.assertEquals('a,NE,b', pretty_tokens(tokenise ("a != b")))
        self.assertEquals('a,AND,b', pretty_tokens(tokenise ("a and b")))
        self.assertEquals('a,OR,b', pretty_tokens(tokenise ("a or b")))
        self.assertEquals('a,CB,OR,OB,b', pretty_tokens(tokenise ("a)or(b")))
        self.assertEquals('NOT,a', pretty_tokens(tokenise ("! a")))
        self.assertEquals('ab,BS,cd', pretty_tokens(tokenise ("ab\\cd")))
        self.assertEquals('work', pretty_tokens(tokenise ('work'))) # Contains an or
        
        self.assertEquals("unclosed quote", catch_exception(lambda: tokenise ('a"b')))
        
    def test_parse_string (self):
        string, tokens = parse_string ([('SP', ' '),('TXT','x'),('TXT','y'),('CB', ')')], 'CB')
        self.assertEquals(' xy', string)
        self.assertEquals('CB', pretty_tokens (tokens))
        
        string, tokens = parse_string ([('SP', ' '),('TXT','x'),('TXT','y')], 'CB')
        self.assertEquals(' xy', string)
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
        
        expr = parse_expr(tokenise ('true and true and true'))[0]
        self.assertTrue(expr (None))
        
        expr = parse_expr(tokenise ('true and true and false'))[0]
        self.assertFalse(expr (None))
        
        expr = parse_expr(tokenise ('true and false and true'))[0]
        self.assertFalse(expr (None))
        
        expr = parse_expr(tokenise ('false and true and true'))[0]
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
        
        expr = parse_expr(tokenise ('false or false or false'))[0]
        self.assertFalse(expr (None))
        
        expr = parse_expr(tokenise ('false or false or true'))[0]
        self.assertTrue(expr (None))
        
        expr = parse_expr(tokenise ('false or true or false'))[0]
        self.assertTrue(expr (None))
        
        expr = parse_expr(tokenise ('true or false or false'))[0]
        self.assertTrue(expr (None))
        
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
    
    def test_parse_expr_missing_brackets (self):
        expr = parse_expr(tokenise ('true=false or true=true))'))[0]
        self.assertTrue(expr (None))
        expr = parse_expr(tokenise ('true=false or true=false))'))[0]
        self.assertFalse(expr (None))
        expr = parse_expr(tokenise ('true=true or true=false))'))[0]
        self.assertTrue(expr (None))
        
    def test_parse_expr_date(self):
        tue = datetime.strptime('Apr 9 2013 11:33PM', '%b %d %Y %I:%M%p')
        wed = datetime.strptime('Apr 10 2013 11:33PM', '%b %d %Y %I:%M%p')
        expr = parse_expr(tokenise ('today'), type_required=STRING_TYPE, now=tue)[0]
        self.assertEquals ("today", expr(None))
        expr = parse_expr(tokenise ('today'), type_required = DATE_TYPE, now=tue)[0]
        self.assertEquals ("2013-04-09", date_range_to_str (expr(None)))
        expr = parse_expr(tokenise ('"last tues"'), type_required = DATE_TYPE, now=tue)[0]
        self.assertEquals ("2013-04-02", date_range_to_str (expr(None)))
        expr = parse_expr(tokenise ('due = today'), now=tue)[0]
        self.assertTrue (expr(Task(name="", date_due=tue)))
        expr = parse_expr(tokenise ('due = start'), now=tue)[0]
        self.assertTrue (expr(Task(name="", date_due=tue, date_to_start=tue)))
        self.assertFalse (expr(Task(name="", date_due=tue, date_to_start=wed)))
        self.assertFalse (expr(Task(name="", date_due=tue)))
        
    def test_parse_expr_type(self):
        expr = parse_expr(tokenise ('type="Task"'))[0]
        self.assertTrue(expr (Task(flagged=True)))
        self.assertFalse(expr (Project(flagged=True)))
        
    def test_parse_expr_status(self):
        expr = parse_expr(tokenise ('status="done"'))[0]
        self.assertTrue(expr (Project(status="done")))
        self.assertFalse(expr (Project(status="active")))
        
    def test_parse_expr_quoted_string_literal(self):
        expr = parse_expr(tokenise ('name="aabbccdd"'))[0]
        self.assertTrue(expr (Task(name="aabbccdd")))
        self.assertFalse(expr (Task(name="zzz")))
        
    def test_parse_expr_unquoted_string_literal(self):
        expr = parse_expr(tokenise ('name=aabbccdd'))[0]
        self.assertTrue(expr (Task(name="aabbccdd")))
        self.assertFalse(expr (Task(name="zzz")))
        
    def test_parse_expr_string_regexp(self):
        expr = parse_expr(tokenise ('name="bb"'))[0]
        self.assertTrue(expr (Task(name="aabbccdd")))
        self.assertFalse(expr (Task(name="zzz")))

    def test_parse_expr_accessing_missing_params (self):
        tue = datetime.strptime('Apr 9 2013 11:33PM', '%b %d %Y %I:%M%p')
        expr = parse_expr(tokenise ('flagged'))[0]
        self.assertFalse(expr (Folder(name="aabbccdd")))
        
        expr = parse_expr(tokenise ('due=today'),now=tue)[0]
        self.assertFalse(expr (Folder(name="aabbccdd")))
        
    def test_bug_2013_04_24 (self):
        expr = parse_expr(tokenise ('(type="Folder") and (name!="^Misc")'))[0]
        self.assertFalse(expr (Folder(name="Miscellaneous")))
        expr = parse_expr(tokenise ('(type="Project") and (name="Misc")'))[0]
        self.assertTrue(expr (Project(name="Miscellaneous")))
        self.assertFalse(expr (Project(name="xxx")))
        expr = parse_expr(tokenise ('((type="Project") and (name="Misc"))'))[0]
        self.assertTrue(expr (Project(name="Miscellaneous")))
        self.assertFalse(expr (Project(name="xxx")))
        self.assertFalse(expr (Folder(name="Misc")))
        
    def test_bug_2013_04_26 (self):
        expr = parse_expr(tokenise ('text=^Work$|^Miscellaneous$'))[0]
        self.assertFalse(expr (Folder(name="Misc")))
        self.assertTrue(expr (Folder(name="Miscellaneous")))
        
        expr = parse_expr(tokenise ('(type=Folder)'))[0]
        self.assertTrue(expr (Folder(name="Miscellaneous")))
        
        expr = parse_expr(tokenise ('(type=Folder)and(text=^Work$|^Miscellaneous$)'))[0]
        self.assertFalse(expr (Folder(name="Misc")))
        self.assertTrue(expr (Folder(name="Miscellaneous")))
    
    def test_bug_2013_04_27 (self):
        expr = parse_expr(tokenise ('(type=Folder) and !name=".*Folder 2"'))[0]
        self.assertTrue(expr (Folder(name="Miscellaneous")))
        self.assertFalse(expr (Folder(name="xxx Folder 2")))
        
        expr = parse_expr(tokenise ('(type=Folder) and name!=".*Folder 2"'))[0]
        self.assertTrue(expr (Folder(name="Miscellaneous")))
        self.assertFalse(expr (Folder(name="xxx Folder 2")))
    
    def test_bug_2013_04_28 (self):
        tue = datetime.strptime('Apr 9 2013 11:33PM', '%b %d %Y %I:%M%p')
        expr = parse_expr(tokenise ("flagged or true"), now=tue)[0]
        self.assertTrue(expr (Project()))
        
        expr = parse_expr(tokenise ("flagged or due=today"), now=tue)[0]
        self.assertFalse(expr (Project()))
        self.assertTrue(expr (Project(flagged=True)))
        self.assertTrue(expr (Project(date_due=tue)))
        
    def test_bug_2013_04_28_2 (self):
        tue = datetime.strptime('Apr 9 2013 11:33PM', '%b %d %Y %I:%M%p')
        expr = parse_expr(tokenise ("flagged or (due='to tomorrow')"), now=tue)[0]
        self.assertFalse(expr (Task()))
        self.assertTrue(expr (Task(flagged=True)))
        self.assertTrue(expr (Task(date_due=tue)))
            
    def test_parse_expr_none(self):
        tue = datetime.strptime('Apr 9 2013 11:33PM', '%b %d %Y %I:%M%p')
        expr = parse_expr(tokenise ('due = none'))[0]
        self.assertTrue (expr(Task(name="")))
        self.assertFalse (expr(Task(name="", date_due=tue)))
        
    def test_parse_expr_any(self):
        tue = datetime.strptime('Apr 9 2013 11:33PM', '%b %d %Y %I:%M%p')
        expr = parse_expr(tokenise ('due = any'))[0]
        self.assertFalse (expr(Task(name="")))
        self.assertTrue (expr(Task(name="", date_due=tue)))
        
    def test_parse_expr_note_filter(self):
        expr = parse_expr(tokenise ('note=123'))[0]
        self.assertTrue(expr (Task(note=TestNote("aaaa123bbb\nccc456ddd"))))
        self.assertTrue(expr (Task(note=TestNote("aaaazzzbbb\nccc123ddd"))))
        self.assertFalse(expr (Task(note=TestNote("z\y\z"))))
        self.assertFalse(expr (Task()))
        
    def test_make_command_filter (self):
        self.assertEquals (None, make_command_filter ("nonsense"))
        self.assertEquals (Sort, type(make_command_filter ("sort Task name")))
        self.assertEquals (Flatten, type(make_command_filter ("flatten Project")))
        self.assertEquals (Prune, type(make_command_filter ("prune Folder")))
        
        self.assertEquals("prune takes one node type argument, got: prune x y", catch_exception(lambda: make_command_filter ("prune x y")))
        self.assertEquals("no such node type in prune: Floder", catch_exception(lambda: make_command_filter ("prune Floder")))
        self.assertEquals("flatten takes one node type argument, got: flatten x y", catch_exception(lambda: make_command_filter ("flatten x y")))
        self.assertEquals("no such node type in flatten: Floder", catch_exception(lambda: make_command_filter ("flatten Floder")))
        self.assertEquals("no such node type in sort: Kangaroo", catch_exception(lambda: make_command_filter ("sort Kangaroo ")))
        self.assertEquals("sort takes two arguments, node type and field, got: sort x y z", catch_exception(lambda: make_command_filter ("sort x y z")))
        self.assertEquals("no such sortable field:weight", catch_exception(lambda: make_command_filter ("sort Task weight")))

    def test_make_expr_filter (self):
        self.assertEquals (Filter, type(make_expr_filter ('type="Context"', True))) 
        
        self.assertEquals("expecting a Boolean got a String: field:name", catch_exception(lambda: make_expr_filter ('name', True)))
        self.assertEquals("expecting a Boolean got a Date: field:date_due", catch_exception(lambda: make_expr_filter ('due', True)))
        self.assertEquals("expecting a Date got a String: field:name", catch_exception(lambda: make_expr_filter ('due = name', True)))
        self.assertEquals('found "name" not: [\'AND\', \'OR\', \'EQ\', \'NE\', \'CB\']', catch_exception(lambda: make_expr_filter ('not name', True)))

