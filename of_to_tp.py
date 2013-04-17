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

class PrintTaskpaperVisitor(Visitor):
    def __init__ (self, out, links = False, depth=0):
        self.depth = depth
        self.out = out
        self.links = links
    def begin_folder (self, folder):
        print >>self.out, self.tabs() + folder.name + ':'
        self.depth+=1
        self.print_link ('folder', folder)
    def end_folder (self, folder):
        self.depth-=1
    def begin_project (self, project):
        if self.project_mode:
            print >>self.out, self.tabs() + project.name + ':' + self.tags(project)
        else:
            print >>self.out, self.tabs() + '- ' + self.remove_trailing_colon(project.name) + self.tags(project)
        self.depth+=1
        self.print_link ('task', project)
    def end_project (self, project):
        self.depth-=1
    def begin_task (self, task):
        if self.is_empty (task) or self.project_mode == False:
            print >>self.out, self.tabs() + '- ' + self.remove_trailing_colon(task.name) + self.tags(task)
        else:
            print >>self.out, self.tabs() + task.name + ':'
        self.depth+=1
    def end_task (self, task):
        self.depth-=1
    def begin_context (self, context):
        print >>self.out, self.tabs() + context.name + ':'
        self.depth+=1
        self.print_link ('context', context)
    def end_context (self, context):
        self.depth-=1
    def tags (self, item):
        tags = []
        if item.date_completed != None:
            tags.append(item.date_completed.strftime("@done(%Y-%m-%d)"))
        else:
            tags.append("@todo")
        if item.flagged:
            tags.append ("@flagged")
        if item.date_to_start != None:
            tags.append(item.date_to_start.strftime("@start(%Y-%m-%d)"))
        if item.date_due != None:
            tags.append (item.date_due.strftime("@due(%Y-%m-%d)"))
        if item.context != None:
            tags.append ('@' + ''.join (item.context.name.split ()))
        if len (tags) > 0:
            return ' ' + ' '.join(tags)
        return ''
    def remove_trailing_colon (self, string):
        if string.endswith(':'):
            return string[:-1]
        return string
    def is_empty (self, item):
        return len ([x for x in item.children if x.marked]) == 0
    def tabs (self):
        return '\t' * (self.depth)
    def print_link (self, link_type, item):
        if self.links and 'persistentIdentifier' in item.ofattribs:
            ident = item.ofattribs['persistentIdentifier']
            link = 'omnifocus:///' + link_type + '/' + ident
            print >>self.out, self.tabs() + link

if __name__ == "__main__":

    root_projects_and_folders, root_contexts = build_model (find_database ())
    
    file_name=os.environ['HOME'] + '/Desktop/OF.taskpaper'
    
    out=codecs.open(file_name, 'w', 'utf-8')
    
    print >>out, 'Projects:'
    traverse_list (PrintTaskpaperVisitor (out, True, depth=1), root_projects_and_folders)
    print >>out, 'Contexts:'
    traverse_list (PrintTaskpaperVisitor (out, False, depth=1), root_contexts, project_mode=False)
    
    out.close()
    
    os.system("open '" + file_name + "'")
