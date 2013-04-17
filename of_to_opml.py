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

class PrintOpmlVisitor(Visitor):
    def __init__ (self, out, depth=2, indent=2, links=True):
        self.depth = depth
        self.out = out
        self.links = links
        self.indent = indent
    def begin_folder (self, folder):
        self.print_node_start ('folder', folder, None)
        self.depth+=1
    def end_folder (self, folder):
        self.depth-=1
        self.print_node_end ()
    def begin_project (self, project):
        self.print_node_start ('task', project, project.date_completed)
        self.depth+=1
    def end_project (self, project):
        self.depth-=1
        self.print_node_end ()
    def begin_task (self, task):
        self.print_node_start ('task', task, task.date_completed)
        self.depth+=1
    def end_task (self, task):
        self.depth-=1
        self.print_node_end ()
    def begin_context (self, context):
        self.print_node_start ('context', context, None)
        self.depth+=1
    def end_context (self, context):
        self.depth-=1
        self.print_node_end ()
    def print_node_start (self, link_type, item, completed):
        print >>self.out, self.spaces() + '<outline text="' +  self.escape(item.name) + '"',
        if completed != None:
            print >>self.out, 'completed="' + completed.strftime ("%Y-%m-%d") + '"',
        if self.links:
            # This happens on "No Context" - we fabricate it and it has no persistentIdentifier
            if 'persistentIdentifier' in item.ofattribs:
                ident = item.ofattribs['persistentIdentifier']
                print >>self.out,'_note="omnifocus:///' + link_type + '/' + ident + '"',
        print >>self.out, ">"
    def print_node_end (self):
        print >>self.out, self.spaces() + '</outline>'
    def spaces (self):
        return ' ' * (self.depth * self.indent)
    def escape (self, val):
        return val.replace('"','&quot;').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')