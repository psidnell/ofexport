from omnifocus import traverse_folder, traverse_contexts, build_model, Visitor
import os
import codecs

class LinkGenVisitor(Visitor):
    def __init__ (self, out, print_tasks, indent=4):
        self.depth = 0
        self.out = out
        self.print_tasks = print_tasks
        self.indent = indent
    def begin_folder (self, folder):
        self.print_link ('folder', folder)
        self.depth+=1
    def end_folder (self, folder):
        self.depth-=1
    def begin_project (self, project):
        if project.date_completed == None and self.print_tasks:
            self.print_link ('task', project)
        self.depth+=1
    def end_project (self, project):
        self.depth-=1
    def begin_task (self, task):
        if task.date_completed == None and self.print_tasks:
            self.print_link ('task', task)
        self.depth+=1
    def end_task (self, task):
        self.depth-=1
    def begin_context (self, context):
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
for folder in folders:
    if folder.name == 'Work':
        traverse_folder (LinkGenVisitor (out, True), folder)
traverse_contexts (LinkGenVisitor (out, False), contexts)
out.close()
os.system("open '" + file_name + "'")