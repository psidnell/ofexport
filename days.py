from omnifocus import Folder, Visitor, traverse_folder, traverse_list, traverse_project, build_model, find_database
import os
import codecs
from datetime import datetime
import sys
from of_to_tp import PrintTaskpaperVisitor
from of_to_md import PrintMarkdownVisitor
from of_to_opml import PrintOpmlVisitor
from of_to_html import PrintHtmlVisitor

DAYS={'0':'Sun', '1':'Mon', '2':'Tue', '3':'Wed', '4':'Thu', '5':'Fri', '6':'Sat'}

'''
Any folder with this name is scanned
'''
folder_to_include = 'Work'

'''
This is the visitor that controls what tasks are in the report.
exclude things outside the completion window, with
'routine' in the project name or unfinished.
'''
class FilterVisitor(Visitor):
    def __init__(self, days=1, root_folder_names=[]):
        self.days = days;
        self.root_folder_names = root_folder_names
    def end_project (self, project):
        marked_tasks = [x for x in project.children if x.marked]
        project.marked = len (marked_tasks) > 0
    def end_folder (self, folder):
        marked_projects = [x for x in folder.children if x.marked]
        folder.marked = len (marked_projects) > 0
        if len(self.root_folder_names) > 0 and not folder.name in self.root_folder_names:
            folder.marked = False
    def end_task (self, task):
        if task.date_completed == None:
            task.marked = False
        elif 'routine' in str(task.project).lower():
            task.marked = False
        else:
            days_elapsed = (datetime.today().date() - task.date_completed.date()).days
            task.marked = days_elapsed < self.days

class CustomPrintTaskpaperVisitor (PrintTaskpaperVisitor):
    def tags (self, completed):
        if completed != None:
            return completed.strftime(" @%Y-%m-%d-%a")
        else:
            return ""
'''
Flatten the projects into a list
'''
class CollectProjectVisitor (Visitor):
    def __init__(self):
        self.projects = []
    def begin_project (self, project):
        self.projects.append(project)
        
def print_structure (visitor, root_projects_and_folders, flat=False):
    for item in root_projects_and_folders:
        if item.__class__ == Folder:
            if flat:
                flattening_visitor = CollectProjectVisitor ()
                traverse_folder (flattening_visitor, item)
                for project in flattening_visitor.projects:
                    traverse_project (visitor, project)
            else:
                traverse_folder (visitor, item)
        else:
            if flat:
                flattening_visitor = CollectProjectVisitor ()
                traverse_project (flattening_visitor, item)
                traverse_project (visitor, item)
            else:
                traverse_folder (visitor, item)
    
if __name__ == "__main__":
    
    today = date.today ()
    time_fmt='%Y-%m-%d'
    days = 1
    fmt = "tp"
    hlp = False
    opn=False
    flat=False
    root_folder_names = []
    
    for arg in sys.argv[1:]:
        if arg[0] == '-':
            if arg[1:] == 'o':
                opn = True
            elif arg[1:] == 'f':
                flat = True
            elif arg[1:] == '?' or arg[1:] == 'h':
                hlp = True
            else:
                fmt = arg[1:]
        else:
            try:
                days = int(arg)
            except ValueError:
                root_folder_names.append(arg)
    
    if hlp:
        print 'usage:'
        print 'days [-fmt] [-f] [-?] [-h] [n] [folder...]'
        print '-h or -?: help'
        print '-f: flatten project structure (no folders)'
        print 'fmt: tp|md|ft|opml|html|week'
        print 'folder: root folder name(s), just descend into named root folders'
        print 'n=number of days in the past'
        exit
        
    root_projects_and_folders, root_contexts = build_model (find_database ())
    
    file_name_base = os.environ['HOME']+'/Desktop/'
    date_str = today.strftime (time_fmt)
    
    # MARKDOWN
    if fmt == 'md':
        file_name = file_name_base + date_str + '.md'
        out=codecs.open(file_name, 'w', 'utf-8')
        
        traverse_list (FilterVisitor (days=days, root_folder_names=root_folder_names), root_projects_and_folders)
        print_structure (PrintMarkdownVisitor (out), root_projects_and_folders, flat=flat)
        
    # FOLDING TEXT
    elif fmt == 'ft':
        file_name = file_name_base + date_str + '.ft'
        out=codecs.open(file_name, 'w', 'utf-8')
        
        traverse_list (FilterVisitor (days=days, root_folder_names=root_folder_names), root_projects_and_folders)
        print_structure (PrintMarkdownVisitor (out), root_projects_and_folders, flat=flat)
                
    # TASKPAPER            
    elif fmt == 'tp':
        file_name = file_name_base + date_str + '.taskpaper'
        out=codecs.open(file_name, 'w', 'utf-8')
        
        traverse_list (FilterVisitor (days=days, root_folder_names=root_folder_names), root_projects_and_folders)
        print_structure (CustomPrintTaskpaperVisitor (out), root_projects_and_folders, flat=flat)
                
    # MARKDOWN WEEKLY REPORT
    elif fmt == 'week':
        days = 7
        flat=True
        file_name = file_name_base + 'week-' + date_str + '.taskpaper'
        root_folder_names = ['Work', 'Miscellaneous']
        out=codecs.open(file_name, 'w', 'utf-8')
        print >>out, 'Weekly Progress Report:'
        print >>out
        print >>out, '\tPaul Sidnell: ' + today.strftime ("%Y-%m-%d")
        print >>out
        print >>out, '\tAccomplishment For This Week:'
        
        traverse_list (FilterVisitor (days=days, root_folder_names=root_folder_names), root_projects_and_folders)
        print_structure (CustomPrintTaskpaperVisitor (out, depth=2), root_projects_and_folders, flat=flat)
        
        print >>out, '\tPlans For Next Week:'
        print >>out, '\t\t- ?'
        print >>out, '\tComments/Issues:'
        print >>out, '\t\t- ?'
    
    # OPML
    elif fmt == 'opml':
        file_name = file_name_base + date_str + '.opml'
        out=codecs.open(file_name, 'w', 'utf-8')
        print >>out, '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        print >>out, '<opml version="1.0">'
        print >>out, '  <head>'
        print >>out, '    <title>OmniFocus</title>'
        print >>out, '  </head>'
        print >>out, '  <body>'
        
        traverse_list (FilterVisitor (days=days, root_folder_names=root_folder_names), root_projects_and_folders)
        print_structure (PrintOpmlVisitor (out, depth=1), root_projects_and_folders, flat=flat)
        
        print >>out, '  </body>'
        print >>out, '</opml>'
        
    # HTML
    elif fmt == 'html':
        file_name = file_name_base + date_str + '.html'
        out=codecs.open(file_name, 'w', 'utf-8')
        print >>out, '<html>'
        print >>out, '  <head>'
        print >>out, '    <title>OmniFocus</title>'
        print >>out, '  </head>'
        print >>out, '  <body>'
        
        traverse_list (FilterVisitor (days=days, root_folder_names=root_folder_names), root_projects_and_folders)
        print_structure (PrintHtmlVisitor (out, depth=1), root_projects_and_folders, flat=flat)
        
        print >>out, '  </body>'
        print >>out, '<html>'
    else:
        raise Exception ('unknown format ' + fmt)
    
    # Close the file and open it
    out.close()
    
    if opn:
        os.system("open '" + file_name + "'")
