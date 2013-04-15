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

import os
import codecs
from treemodel import traverse_list, Visitor
from omnifocus import build_model, find_database

class PrintTextVisitor(Visitor):
    def __init__ (self, out, indent=4):
        self.depth = 0
        self.indent = indent
        self.out = out
    def begin_folder (self, folder):
        print >>self.out, self.spaces() + '* Folder: ' + folder.name
        self.depth+=1
    def end_folder (self, folder):
        self.depth-=1
    def begin_project (self, project):
        print >>self.out, self.spaces () + '* Project: ' + str(project) + self.attribs (project)
        self.depth+=1
    def end_project (self, project):
        self.depth-=1
    def begin_task (self, task):
        print >>self.out, self.spaces() + '* Task: ' + task.name + self.attribs (task)
        self.depth+=1
    def end_task (self, task):
        self.depth-=1
    def begin_context (self, context):
        print >>self.out, self.spaces() + '* Context: ' + context.name
        self.depth+=1
    def end_context (self, context):
        self.depth-=1
    def attribs (self, task):
        attribs = []
        if task.date_completed != None:
            attribs.append ('Done:' + task.date_completed.strftime ('%Y-%m-%d'))
        if task.flagged:
            attribs.append ('Flagged')
        if len (attribs) > 0:
            return ' ' +  ' '.join(attribs)
        return ''
    def spaces (self):
        return ' ' * self.depth * self.indent
    
if __name__ == "__main__":
    file_name=os.environ['HOME'] + '/Desktop/OF.txt'
    
    out=codecs.open(file_name, 'w', 'utf-8')
     
    visitor = PrintTextVisitor (out)
    root_projects_and_folders, root_contexts = build_model (find_database ())
    traverse_list (visitor, root_projects_and_folders)
    traverse_list (visitor, root_contexts, project_mode=False)
        
    os.system("open '" + file_name + "'")
    
    out.close()