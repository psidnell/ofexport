from omnifocus import traverse_folders, traverse_contexts, build_model, Visitor, find_database
import os
import codecs

'''
This is a visitor that dumps out an OPML file containing each and every entry
in the database. You can also specify a particular type, e.g. just 'Task'.
'''
class OPMLVisitor(Visitor):
    def __init__ (self, out, types = {'Folder', 'Project', 'Task'}, indent=0):
        self.depth = 0
        self.out = out
        self.types = types
        self.indent = indent
    def begin_folder (self, folder):
        if 'Folder' in self.types:
            self.print_node_start ('folder', folder)
        self.depth+=1
    def end_folder (self, folder):
        self.depth-=1
        if 'Folder' in self.types:
            self.print_node_end ()
    def begin_project (self, project):
        if project.date_completed == None and 'Project' in self.types:
            self.print_node_start ('task', project)
        self.depth+=1
    def end_project (self, project):
        self.depth-=1
        if project.date_completed == None and 'Project' in self.types:
            self.print_node_end ()
    def begin_task (self, task):
        if task.date_completed == None and 'Task' in self.types:
            self.print_node_start ('task', task)
        self.depth+=1
    def end_task (self, task):
        self.depth-=1
        if task.date_completed == None and 'Task' in self.types:
            self.print_node_end ()
    def begin_context (self, context):
        if 'Context' in self.types:
            self.print_node_start ('context', context)
        self.depth+=1
    def end_context (self, context):
        self.depth-=1
        if 'Context' in self.types:
            self.print_node_end ()
    def print_node_start (self, link_type, item):
        print >>self.out, self.spaces() + '<outline text="' +  str(item.__class__.__name__) + ':' + self.escape(item.name) + '">'
        # add a URL to the OF entry as a child
        print >>self.out, self.spaces() + '  <outline text="omnifocus:///' + link_type + '/' + item.persistent_identifier + '"/>'
    def print_node_end (self):
        print >>self.out, self.spaces() + '</outline>'
    def spaces (self):
        return '  ' * (self.depth + self.indent)
    def escape (self, val):
        return val.replace('"','&quot;').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

folders, contexts = build_model (find_database ())

file_name=os.environ['HOME'] + '/Desktop/OF.opml'

out=codecs.open(file_name, 'w', 'utf-8')

print >>out, '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
print >>out, '<opml version="1.0">'
print >>out, '  <head>'
print >>out, '    <title>OmniFocus</title>'
print >>out, '  </head>'
print >>out, '  <body>'
print >>out, '    <outline text="OmniFocus">'
print >>out, '      <outline text="Projects">'
traverse_folders (OPMLVisitor (out, types ={'Folder','Project','Task'}, indent=4), folders)
print >>out, '      </outline>'
print >>out, '      <outline text="Contexts">'
traverse_contexts (OPMLVisitor (out, types={'Context','Task'}, indent=4), contexts)
print >>out, '      </outline>'
print >>out, '    </outline>'
print >>out, '  </body>'
print >>out, '</opml>'

out.close()

os.system("open '" + file_name + "'")