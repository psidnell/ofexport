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

from treemodel import Visitor
from fmt_template import FmtTemplate, format_item

from string import replace

DEFAULT_TEMPLATE = {
                        'indentStart'           : 0,
                        'indent'                : '\t',
                        'Nodes': {
                              'Project'         : '$name:$flagged$date_to_start$date_due$date_completed$context$project',
                              'Folder'          : '$name:',
                              'Context'         : '$name:',
                              'Task'            : '- $name $flagged$date_to_start$date_due$date_completed$context$project',
                              'TaskGroup'       : '$name:$tags',
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

def remove_trailing_colon (x):
    if x.endswith(':'):
        return x[:-1]
    return x
    
def strip_brackets (x):
    return replace(replace(x, ')', ''), '(','')
    
ATTRIB_CONVERSIONS = {
                      'name'           : lambda x: remove_trailing_colon(x),
                      'flagged'        : lambda x: str(x) if x else None,
                      'context'        : lambda x: strip_brackets(''.join (x.name.split ())),
                      'project'        : lambda x: strip_brackets(''.join (x.name.split ())),
                      'date_to_start'  : lambda x: x.strftime('%Y-%m-%d'),
                      'date_due'       : lambda x: x.strftime('%Y-%m-%d'),
                      'date_completed' : lambda x: x.strftime('%Y-%m-%d')
                      }
    
class PrintTaskpaperVisitor(Visitor):
    def __init__ (self, out, links = False, template = FmtTemplate(DEFAULT_TEMPLATE)):
        self.template = template
        self.depth = self.template.indent_start
        self.out = out
        self.links = links
    def begin_folder (self, folder):
        line = format_item (folder, self.template, 'Folder', ATTRIB_CONVERSIONS)
        print >>self.out, self.indent() + line
        self.depth+=1
        self.print_link ('folder', folder)
    def end_folder (self, folder):
        self.depth-=1
    def begin_project (self, project):
        line = format_item (project, self.template, 'Project', ATTRIB_CONVERSIONS)
        print >>self.out, self.indent() + line
        self.depth+=1
        self.print_link ('task', project)
    def end_project (self, project):
        self.depth-=1
    def begin_task (self, task):
        if self.is_empty (task) or self.project_mode == False:
            line = format_item (task, self.template, 'Task', ATTRIB_CONVERSIONS)
            print >>self.out, self.indent() + line
        else:
            line = format_item (task, self.template, 'TaskGroup', ATTRIB_CONVERSIONS)
            print >>self.out, self.indent() + line
        self.depth+=1
    def end_task (self, task):
        self.depth-=1
    def begin_context (self, context):
        line = format_item (context, self.template, 'Context', ATTRIB_CONVERSIONS)
        print >>self.out, self.tabs() + line
        self.depth+=1
        self.print_link ('context', context)
    def end_context (self, context):
        self.depth-=1
    def is_empty (self, item):
        return len ([x for x in item.children if x.marked]) == 0
    def indent (self):
        return self.template.indent * (self.depth)
    def print_link (self, link_type, item):
        if self.links and 'persistentIdentifier' in item.ofattribs:
            ident = item.ofattribs['persistentIdentifier']
            link = 'omnifocus:///' + link_type + '/' + ident
            print >>self.out, self.indent() + link