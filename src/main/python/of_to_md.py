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

from fmt_template import Formatter

class PrintMarkdownVisitor(Formatter):
    def __init__ (self, out, template):
        Formatter.__init__(self, out, template)
        self.header_depth = 0
        self.depth = 0
        self.out = out
        self.last_line_was_text = False
    def begin_folder (self, folder):
        if self.last_line_was_text:
            print >> self.out
        print >>self.out, ('#' * (self.header_depth+1)),
        Formatter.begin_folder(self, folder)
        print >>self.out
        self.depth = 0
        self.header_depth+=1
        self.last_line_was_text = False
    def begin_project (self, project):
        if self.last_line_was_text:
            print >> self.out
        print >>self.out, ('#' * (self.header_depth+1)),
        Formatter.begin_project(self, project)
        print >>self.out
        self.depth = 0
        self.header_depth+=1
        self.last_line_was_text = False
    def begin_context (self, context):
        if self.last_line_was_text:
            print >> self.out
        print >>self.out, ('#' * (self.header_depth+1)),
        Formatter.begin_context(self, context)
        print >>self.out
        self.depth = 0
        self.header_depth+=1
        self.last_line_was_text = False
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
