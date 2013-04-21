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
from treemodel import Task
from datetime import datetime
from fmt_template import FmtTemplate, format_item, build_attrib_values, build_template_substitutions, build_entry
from string import Template

TAGS_TEMPLATE = Template ('$flagged$date_to_start$date_due$date_completed$context$project')

ATTRIB_TEMPLATES = {
                      'name'           : Template ('$value'),
                      'flagged'        : Template (' @flagged'),
                      'date_to_start'  : Template (' @start($value)'),
                      'date_due'       : Template (' @due($value)'),
                      'date_completed' : Template (' @done($value)'),
                      'context'        : Template (' @context($value)'),
                      'project'        : Template (' @start($value)')
                      }

ATTRIB_CONVERSIONS = {
                      'name'           : lambda x: str (x),
                      'flagged'        : lambda x: str(x) if x else None,
                      'context'        : lambda x: ''.join (x.name.split ()),
                      'project'        : lambda x: ''.join (x.name.split ()),
                      'date_to_start'  : lambda x: x.strftime('%Y-%m-%d'),
                      'date_due'       : lambda x: x.strftime('%Y-%m-%d'),
                      'date_completed' : lambda x: x.strftime('%Y-%m-%d')
                      }

ATTRIB_DEFAULTS = {
                      'name'           : '',
                      'flagged'        : '',
                      'context'        : '',
                      'project'        : '',
                      'date_to_start'  : '',
                      'date_due'       : '',
                      'date_completed' : '',
                      }


DEFAULT_TEMPLATE = {
                        'indentStart'           : 0,
                        'indent'                : 0,
                        'indentString'          : '\t',
                        'depth'                 : 0,
                        'Nodes'                 : {
                              'ProjectStart'    : 'P $name:$flagged$date_to_start$date_due$date_completed$context$project',
                              'FolderStart'     : 'F $name:',
                              'ContextStart'    : 'C $name:',
                              'TaskStart'       : 'T $name$flagged$date_to_start$date_due$date_completed$context$project',
                              'TaskGroupStart'  : 'T $name:$flagged$date_to_start$date_due$date_completed$context$project',
                              },
                        'NodeAttributes'        : {
                              'name'            : '$value',
                              'flagged'         : ' @flagged',
                              'date_to_start'   : ' @start($value)',
                              'date_due'        : ' @due($value)',
                              'date_completed'  : ' @done($value)',
                              'context'         : ' @context($value)',
                              'project'         : ' @project($value)'
                            },
                        'NodeAttributeDefaults' : {
                              'name'            : '',
                              'flagged'         : '',
                              'context'         : '',
                              'project'         : '',
                              'date_to_start'   : '',
                              'date_due'        : '',
                              'date_completed'  : ''
                              }
                    }

class Test_fmt_datematch(unittest.TestCase):
    
    def test_build_attrib_values (self):
        task = Task (name='My Name', flagged=True, date_completed=datetime.strptime('2015-02-03', '%Y-%m-%d'))
        values = build_attrib_values (task, ATTRIB_CONVERSIONS)
        self.assertEquals(3, len (values))
        self.assertEquals ('My Name', values['name'])
        self.assertEquals ('2015-02-03', values['date_completed'])
        self.assertEquals ('True', values['flagged'])
        
        task = Task (name='My Name', flagged=False, date_completed=datetime.strptime('2015-02-03', '%Y-%m-%d'))
        values = build_attrib_values (task, ATTRIB_CONVERSIONS)
        self.assertEquals(2, len (values))
        self.assertEquals ('My Name', values['name'])
        self.assertEquals ('2015-02-03', values['date_completed'])
        
    def test_build_template_substitutions (self):
        task = Task (name='My Name', flagged=True, date_completed=datetime.strptime('2015-02-03', '%Y-%m-%d'))
        values = build_template_substitutions (task, ATTRIB_CONVERSIONS, ATTRIB_DEFAULTS, ATTRIB_TEMPLATES)
        self.assertEquals(7, len (values))
        self.assertEquals ('My Name', values['name'])
        self.assertEquals (' @done(2015-02-03)', values['date_completed'])
        self.assertEquals (' @flagged', values['flagged'])
        self.assertEquals ('', values['context'])
        self.assertEquals ('', values['date_to_start'])
        self.assertEquals ('', values['date_due'])
        self.assertEquals ('', values['project'])
        
        task = Task (name='My Name', flagged=False, date_completed=datetime.strptime('2015-02-03', '%Y-%m-%d'))
        values = build_template_substitutions (task, ATTRIB_CONVERSIONS, ATTRIB_DEFAULTS, ATTRIB_TEMPLATES)
        self.assertEquals(7, len (values))
        self.assertEquals ('My Name', values['name'])
        self.assertEquals (' @done(2015-02-03)', values['date_completed'])
        self.assertEquals ('', values['context'])
        self.assertEquals ('', values['date_to_start'])
        self.assertEquals ('', values['date_due'])
        self.assertEquals ('', values['project'])
        self.assertEquals ('', values['flagged'])
        
    def test_build_entry (self):
        task = Task (name='My Name', flagged=True, date_completed=datetime.strptime('2015-02-03', '%Y-%m-%d'))
        line = build_entry (task, TAGS_TEMPLATE, ATTRIB_CONVERSIONS, ATTRIB_DEFAULTS, ATTRIB_TEMPLATES)
        self.assertEquals(" @flagged @done(2015-02-03)", line)
    
    def test_format_item (self):
        task = Task (name='My Name', flagged=True, date_completed=datetime.strptime('2015-02-03', '%Y-%m-%d'))
        template = FmtTemplate(DEFAULT_TEMPLATE)
        line = format_item (task, template, 'TaskStart', ATTRIB_CONVERSIONS)
        self.assertEquals ('T My Name @flagged @done(2015-02-03)', line)