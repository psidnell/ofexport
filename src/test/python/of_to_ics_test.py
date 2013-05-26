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
from plugin_ics import fix_dates, load_note_attribs, utc, format_date, format_alarm
from treemodel import Task, Note
from datetime import datetime
import dateutil.parser

class TestNote (Note):
    def __init__ (self, text):
        self.text = text
        self.lines = text.split('\n')
    def get_note (self):
        return self.text
    def get_note_lines (self):
        return self.lines
    
class Test_fmt_datematch(unittest.TestCase):
    
    def test_fix_dates (self):
        tue = datetime.strptime('Apr 9 2013 11:33PM', '%b %d %Y %I:%M%p')
        wed = datetime.strptime('Apr 10 2013 11:33PM', '%b %d %Y %I:%M%p')
        
        task = Task ()
        fix_dates (task)
        self.assertEquals(None, task.date_to_start)
        self.assertEquals(None, task.date_due)
        
        task = Task (date_to_start=tue)
        fix_dates (task)
        self.assertEquals(tue, task.date_to_start)
        self.assertEquals(tue, task.date_due)
        
        task = Task (date_due=tue)
        fix_dates (task)
        self.assertEquals(tue, task.date_to_start)
        self.assertEquals(tue, task.date_due)
        
        task = Task (date_to_start=tue, date_due=wed)
        fix_dates (task)
        self.assertEquals(tue, task.date_to_start)
        self.assertEquals(wed, task.date_due)
        
    def test_load_note_attribs (self):
        task = Task ()
        n_attribs_before = len (task.attribs)
        load_note_attribs (task)
        self.assertEqual (n_attribs_before, len (task.attribs))
        
        n_attribs_before = len (task.attribs)
        task = Task (note=TestNote("xyz"))
        self.assertEqual (n_attribs_before, len (task.attribs))
        
        task = Task (note=TestNote("%of cal xxx"))
        load_note_attribs (task)
        self.assertEquals (True, task.attribs['xxx'])
        
        task = Task (note=TestNote("%of cal xxx\n%of cal yyy"))
        load_note_attribs (task)
        self.assertEquals (True, task.attribs['xxx'])
        self.assertEquals (True, task.attribs['yyy'])
        
        task = Task (note=TestNote("%of cal xxx   yyy zzz   "))
        n_attribs_before = len (task.attribs)
        load_note_attribs (task)
        self.assertEquals (True, task.attribs['xxx'])
        self.assertEquals (True, task.attribs['yyy'])
        self.assertEquals (True, task.attribs['zzz'])
        self.assertEqual (n_attribs_before + 3, len (task.attribs))
        
    def test_load_note_start_attrib (self):
        the_date = dateutil.parser.parse('Wed, 27 Oct 2010 22:17:00 BST')
        task = Task (date_to_start=the_date, date_due=the_date, note=TestNote("%of cal start=18:12"))
        load_note_attribs (task)
        self.assertEqual ("2010.10.27 18:12", task.date_to_start.strftime ('%Y.%m.%d %H:%M'))
        self.assertEqual ("2010.10.27 22:17", task.date_due.strftime ('%Y.%m.%d %H:%M'))
        
    def test_load_note_due_attrib (self):
        the_date = dateutil.parser.parse('Wed, 27 Oct 2010 22:17:00 BST')
        task = Task (date_to_start=the_date, date_due=the_date, note=TestNote("%of cal due=23:12"))
        load_note_attribs (task)
        self.assertEqual ("2010.10.27 22:17", task.date_to_start.strftime ('%Y.%m.%d %H:%M'))
        self.assertEqual ("2010.10.27 23:12", task.date_due.strftime ('%Y.%m.%d %H:%M'))
        
    def test_utc (self):
        the_date = dateutil.parser.parse('Wed, 27 Oct 2010 22:17:00 BST')
        self.assertEquals ("2010.10.27 22:17 BST", the_date.strftime ('%Y.%m.%d %H:%M %Z'))
        self.assertEquals ("2010.10.27 21:17", utc(the_date).strftime ('%Y.%m.%d %H:%M'))
        
        the_date = dateutil.parser.parse('Wed, 27 Oct 2010 22:17:00 UTC')
        self.assertEquals ("2010.10.27 22:17 UTC", the_date.strftime ('%Y.%m.%d %H:%M %Z'))
        self.assertEquals ("2010.10.27 22:17", utc(the_date).strftime ('%Y.%m.%d %H:%M'))
        
    def test_format_date (self):
        wed = dateutil.parser.parse('Wed, 27 Oct 2010 22:17:00 BST')
        thu = dateutil.parser.parse('Thu, 28 Oct 2010 22:17:00 BST')
        
        task = Task (date_to_start=wed, date_due=thu)
        self.assertEquals ("20101027T211700Z", format_date (task, task.date_to_start, False))
        self.assertEquals ("20101028T211700Z", format_date (task, task.date_due, True))
        
        task = Task (date_to_start=wed, date_due=thu)
        task.attribs["allday"] = True
        self.assertEquals ("20101027", format_date (task, task.date_to_start, False))
        self.assertEquals ("20101029", format_date (task, task.date_due, True))
        
        wed1 = dateutil.parser.parse('Wed, 27 Oct 2010 00:00:00 BST')
        wed2 = dateutil.parser.parse('Wed, 27 Oct 2010 23:59:59 BST')
        task = Task (date_to_start=wed1, date_due=wed2)
        task.attribs["allday"] = True
        self.assertEquals ("20101027", format_date (task, task.date_to_start, False))
        self.assertEquals ("20101028", format_date (task, task.date_due, True))
        
        wed1 = dateutil.parser.parse('Wed, 27 Oct 2010 00:00:00 BST')
        wed2 = dateutil.parser.parse('Wed, 28 Oct 2010 00:00:00 BST')
        task = Task (date_to_start=wed1, date_due=wed2)
        task.attribs["allday"] = True
        self.assertEquals ("20101027", format_date (task, task.date_to_start, False))
        self.assertEquals ("20101029", format_date (task, task.date_due, True))
        
    def test_format_alarm (self):
        task = Task ()
        self.assertEquals ("BEGIN:VALARM\nACTION:DISPLAY\nDESCRIPTION:OmniFocus Reminder\nTRIGGER:-PT0M\nEND:VALARM\n", format_alarm (task))
        
        task.attribs['noalarm'] = True
        self.assertEquals ("", format_alarm (task))

        