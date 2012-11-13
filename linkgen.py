from omnifocus import traverse_folders, traverse_contexts, build_model, Visitor
import os
import codecs

class LinkGenVisitor(Visitor):
    def __init__ (self, out, types = {'Folder', 'Project', 'Task'}, indent=4):
        self.depth = 0
        self.out = out
        self.types = types
        self.indent = indent
    def begin_folder (self, folder):
        if 'Folder' in self.types:
            self.print_link ('folder', folder)
        self.depth+=1
    def end_folder (self, folder):
        self.depth-=1
    def begin_project (self, project):
        if project.date_completed == None and 'Project' in self.types:
            self.print_link ('task', project)
        self.depth+=1
    def end_project (self, project):
        self.depth-=1
    def begin_task (self, task):
        if task.date_completed == None and 'Task' in self.types:
            self.print_link ('task', task)
        self.depth+=1
    def end_task (self, task):
        self.depth-=1
    def begin_context (self, context):
        if 'Context' in self.types:
            self.print_link ('context', context)
        self.depth+=1
    def end_context (self, context):
        self.depth-=1
    def print_link (self, link_type, item):
        print >>self.out, self.spaces() + str(item.__class__.__name__) + ': <a href="omnifocus:///' + link_type + '/' + item.persistent_identifier + '">' + item.name + '</a><br>'
    def spaces (self):
        return '&nbsp' * self.depth * self.indent


folders, contexts = build_model ('/Users/psidnell/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2')

file_name='/Users/psidnell/Documents/oflinks.html'

out=codecs.open(file_name, 'w', 'utf-8')

traverse_folders (LinkGenVisitor (out, types ={'Folder', 'Project'}), folders)
print >>out, '<hr/>'

traverse_contexts (LinkGenVisitor (out, types={'Context'}), contexts)
print >>out, '<hr/>'

traverse_folders (LinkGenVisitor (out, types ={'Folder','Project','Task'}), folders)

out.close()

os.system("open '" + file_name + "'")