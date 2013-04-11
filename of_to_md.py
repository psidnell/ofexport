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

from treemodel import traverse_list, Visitor
from omnifocus import build_model, find_database
import os
import codecs

'''
This is a visitor that dumps out an OPML file containing each and every entry
in the database. You can also specify a particular type, e.g. just 'Task'.
'''
class PrintMarkdownVisitor(Visitor):
    def __init__ (self, out, depth=0):
        self.header_depth = depth
        self.task_depth = 0
        self.out = out
    def begin_folder (self, folder):
        self.task_depth = 0
        print >>self.out, ('#' * (self.header_depth+1)) + ' ' + folder.name
        self.header_depth+=1
    def end_folder (self, folder):
        self.header_depth-=1
    def begin_project (self, project):
        self.task_depth = 0
        print >>self.out, ('#' * (self.header_depth+1)) + ' ' + project.name
        self.header_depth+=1
    def end_project (self, project):
        print >>self.out
        self.header_depth-=1
    def begin_task (self, task):
        print >>self.out, (' ' * (4 * self.task_depth)) + '* ' + task.name + self.done(task.date_completed)
        self.task_depth+=1
    def end_task (self, task):
        self.task_depth-=1
    def begin_context (self, context):
        self.task_depth = 0
        print >>self.out, ('#' * (self.header_depth+1)) + ' ' + context.name
        self.header_depth+=1
    def end_context (self, context):
        print >>self.out
        self.header_depth-=1
    def done (self, completed):
        if completed != None:
            return completed.strftime(" @%Y-%m-%d-%a")
        return ""

if __name__ == "__main__":

    root_projects_and_folders, root_contexts = build_model (find_database ())
    
    file_name=os.environ['HOME'] + '/Desktop/OF.md'
    
    out=codecs.open(file_name, 'w', 'utf-8')
    
    print >>out, '# Projects:'
    traverse_list (PrintMarkdownVisitor (out, depth=1), root_projects_and_folders)
    print >>out, '# Contexts:'
    traverse_list (PrintMarkdownVisitor (out, depth=1), root_contexts)
    
    out.close()
    
    os.system("open '" + file_name + "'")