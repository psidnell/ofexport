from fmt_template import Formatter

def escape (val):
    return val.replace('"','&quot;').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    
ATTRIB_CONVERSIONS = {
                      'name'           : lambda x: escape(x),
                      'flagged'        : lambda x: str(x) if x else None,
                      'context'        : lambda x: escape(''.join (x.name.split ())),
                      'project'        : lambda x: escape(''.join (x.name.split ())),
                      'date_to_start'  : lambda x: x.strftime('%Y-%m-%d'),
                      'date_due'       : lambda x: x.strftime('%Y-%m-%d'),
                      'date_completed' : lambda x: x.strftime('%Y-%m-%d')
                      }

class PrintOpmlVisitor(Formatter):
    def __init__ (self, out, template):
        Formatter.__init__(self, out, template, attrib_conversions = ATTRIB_CONVERSIONS)
        
''' Reminder for when I put links back:
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
'''