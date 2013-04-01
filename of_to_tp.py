from omnifocus import traverse_list, traverse_contexts, build_model, Visitor, find_database
import os
import codecs

'''
This is a visitor that dumps out an OPML file containing each and every entry
in the database. You can also specify a particular type, e.g. just 'Task'.
'''
class PrintTaskpaperVisitor(Visitor):
    def __init__ (self, out, depth=0):
        self.depth = depth
        self.out = out
    def begin_folder (self, folder):
        print >>self.out, self.tabs() + folder.name + ':'
        self.depth+=1
    def end_folder (self, folder):
        self.depth-=1
    def begin_project (self, project):
        print >>self.out, self.tabs() + project.name + ':'
        self.depth+=1
    def end_project (self, project):
        self.depth-=1
    def begin_task (self, task):
        if len(task.children) == 0:
            print >>self.out, self.tabs() + '- ' + task.name + self.tags(task.date_completed)
        else:
            print >>self.out, self.tabs() + task.name + ':'
        self.depth+=1
    def end_task (self, task):
        self.depth-=1
    def begin_context (self, context):
        print >>self.out, self.tabs() + context.name + ':'
        self.depth+=1
    def end_context (self, context):
        self.depth-=1
    def tags (self, completed):
        if completed != None:
            return completed.strftime(" @done(%Y-%m-%d-%a)")
        else:
            return " @todo"
    def tabs (self):
        return '\t' * (self.depth)

if __name__ == "__main__":

    root_projects_and_folders, root_contexts = build_model (find_database ())
    
    file_name=os.environ['HOME'] + '/Desktop/OF.taskpaper'
    
    out=codecs.open(file_name, 'w', 'utf-8')
    
    print >>out, 'Projects:'
    traverse_list (PrintTaskpaperVisitor (out, depth=1), root_projects_and_folders)
    print >>out, 'Contexts:'
    traverse_contexts (PrintTaskpaperVisitor (out, depth=1), root_contexts)
    
    out.close()
    
    os.system("open '" + file_name + "'")