from omnifocus import traverse_folders, traverse_contexts, build_model, Visitor, find_database
import os
import codecs

'''
This is a visitor that dumps out html references to each and every entry
in the database. You can also specify a particular type, e.g. just 'Task'.
'''
class PrintHtmlVisitor(Visitor):
    def __init__ (self, out, depth=2, indent=4):
        self.depth = depth
        self.out = out
        self.indent = indent
    def begin_folder (self, folder):
        self.print_link ('folder', folder)
        self.depth+=1
    def end_folder (self, folder):
        self.depth-=1
    def begin_project (self, project):
        self.print_link ('task', project)
        self.depth+=1
    def end_project (self, project):
        self.depth-=1
    def begin_task (self, task):
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
        print >>self.out, self.spaces() + self.escape(str(item.__class__.__name__)) + ': <a href="omnifocus:///' + link_type + '/' + item.persistent_identifier + '">' + self.escape(item.name) + '</a><br>'
    def spaces (self):
        return '&nbsp' * self.depth * self.indent
    def escape (self, val):
        return val.replace('"','&quot;').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

if __name__ == "__main__":
    folders, contexts = build_model (find_database ())
    
    file_name=os.environ['HOME'] + '/Desktop/OF.html'
    
    out=codecs.open(file_name, 'w', 'utf-8')
    print >>out, '<head><title>Omnifocus</title></head><body>'
    traverse_folders (PrintHTMLVisitor (out), folders)
    print >>out, '<hr/>'
    
    traverse_contexts (PrintHTMLVisitor (out), contexts)
    print >>out, '<hr/>'
    print >>out, '</body>'
    out.close()
    
    os.system("open '" + file_name + "'")