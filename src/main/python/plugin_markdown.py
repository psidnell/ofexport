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

from fmt_template import Formatter, format_document
from treemodel import PROJECT
from ofexport import load_template

def generate (out, root_project, root_context, project_mode, template_dir, type_config):
    subject = root_project if project_mode else root_context
    template = load_template (template_dir, type_config['template'])
    visitor = PrintMarkdownVisitor (out, template)
    format_document (subject, visitor, project_mode)

class PrintMarkdownVisitor(Formatter):
    # All this nonsense is just to get the right number of 
    # blank lines in the right places
    def __init__ (self, out, template):
        Formatter.__init__(self, out, template)
        self.header_depth = 0
        self.depth = 0
        self.out = out
        self.last_line_was_text = False
    def begin_folder (self, folder):
        is_output = 'FolderStart' in self.template.nodes
        if self.last_line_was_text and is_output:
            print >> self.out
            self.last_line_was_text = False
        Formatter.begin_folder(self, folder)
        if is_output:
            print >>self.out
        self.depth = 0
        self.header_depth+=1
    def begin_project (self, project):
        is_output = 'ProjectStart' in self.template.nodes
        if self.last_line_was_text and is_output:
            print >> self.out
            self.last_line_was_text = False
        Formatter.begin_project(self, project)
        if is_output:
            print >>self.out
        self.depth = 0
        self.header_depth+=1
    def begin_context (self, context):
        is_output = 'ContextStart' in self.template.nodes
        if self.last_line_was_text and is_output:
            print >> self.out
            self.last_line_was_text = False
        Formatter.begin_context(self, context)
        if is_output:
            print >>self.out
        self.depth = 0
        self.header_depth+=1
    def end_task (self,task):
        Formatter.end_task(self, task)
        self.last_line_was_text = True
    def end_context (self, context):
        self.header_depth-=1
        Formatter.end_context(self, context)
    def end_project (self, project):
        self.header_depth-=1
        Formatter.end_project(self, project)
    def end_folder (self, folder):
        self.header_depth-=1
        Formatter.end_folder(self, folder)
    def handle_note (self, item):
        if item.note != None and 'NoteLine' in self.template.nodes:
            if item.type == PROJECT:
                print >>self.out
            Formatter.handle_note (self, item)
    def add_extra_template_attribs (self, item, attribs):
        attribs['hashes'] = '#' * (self.header_depth+1) + ' '
