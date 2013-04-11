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
        print >>self.out, self.spaces () + '* Project: ' + str(project)
        self.print_task_attribs (project);
        self.depth+=1
    def end_project (self, project):
        self.depth-=1
    def begin_task (self, task):
        print >>self.out, self.spaces() + '* Task: ' + task.name
        self.print_task_attribs (task);
        self.depth+=1
    def end_task (self, task):
        self.depth-=1
    def begin_context (self, context):
        print >>self.out, self.spaces() + '* Context: ' + context.name
        self.depth+=1
    def end_context (self, context):
        self.depth-=1
    def print_task_attribs (self, task):
        # Tasks and projects have same attribs
        print >>self.out, self.spaces () + '  - Context: ' + str(task.context)
        print >>self.out, self.spaces () + '  - DateCompleted: ' + str(task.date_completed)
        print >>self.out, self.spaces () + '  - StartDate: ' + str(task.date_to_start)
        print >>self.out, self.spaces () + '  - Due: ' + str(task.date_due)
        print >>self.out, self.spaces () + '  - Flagged: ' + str(task.flagged)
    def spaces (self):
        return ' ' * self.depth * self.indent
    
if __name__ == "__main__":
    file_name=os.environ['HOME'] + '/Desktop/OF.txt'
    
    out=codecs.open(file_name, 'w', 'utf-8')
     
    visitor = PrintTextVisitor (out)
    root_projects_and_folders, root_contexts = build_model (find_database ())
    traverse_list (visitor, root_projects_and_folders)
    traverse_list (visitor, root_contexts)
        
    os.system("open '" + file_name + "'")
    
    out.close()