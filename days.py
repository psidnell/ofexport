'''
usage:

days [-fmt] [n]

fmt=tp|md|ft|opml|html
n=number of days in the past

'''

from omnifocus import Visitor, traverse_folder, build_model, find_database
import os
import codecs
from datetime import date
import sys

today = date.today ()

DAYS={'0':'Sun', '1':'Mon', '2':'Tue', '3':'Wed', '4':'Thu', '5':'Fri', '6':'Sat'}
time_fmt='%Y-%m-%d'
days = 1
fmt = "opml"

def include_completed_logged (task):
    if task.date_completed == None:
        return False
    if str(task.context).startswith('Log') or str(task.context).startswith('Comments'):
        days_elapsed = (date.today() - task.date_completed).days
        return days_elapsed < days
    return False

class DoneVisitor(Visitor):
    def __init__ (self, out, inclusion_filter, project_printer):
        self.tasks = []
        self.out = out
        self.inclusion_filter = inclusion_filter
        self.project_printer = project_printer
    def end_project (self, project):
        if len(self.tasks) > 0:
            self.tasks.sort(key=lambda task:task.date_completed)
            self.project_printer (self.out, project, self.tasks)
        self.tasks = []
    def begin_task (self, task):
        if self.inclusion_filter(task):
            self.tasks.append (task)

def xml_escape (val):
        return val.replace('"','&quot;').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    
def tp_project_printer (out, project, tasks):
    print >>out, str(project) + ':'
    for task in tasks:
        print >>out, '\t-', task.name, '-', DAYS[task.date_completed.strftime('%w')] + ' @' + task.date_completed.strftime (time_fmt) + ' ' # trailing space in case of :
    
def tp_weekly_project_printer (out, project, tasks):
    print >>out, '\t\t' + str(project) + ':'
    for task in tasks:
        print >>out, '\t\t\t-', task.name, '-', DAYS[task.date_completed.strftime('%w')] + ' @' + task.date_completed.strftime (time_fmt)  + ' ' # trailing space in case of :

def md_project_printer (out, project, tasks):
    print >>out, '#', str(project)
    for task in tasks:
        print >>out, '-', task.name, '-', DAYS[task.date_completed.strftime('%w')] + ' @' + task.date_completed.strftime (time_fmt)
    print >>out
    
def ft_project_printer (out, project, tasks):
    print >>out, '#', str(project)
    for task in tasks:
        print >>out, '-', task.name, '-', DAYS[task.date_completed.strftime('%w')] + ' @completed(' + task.date_completed.strftime (time_fmt) + ')'
    print >>out

def opml_project_printer (out, project, tasks):
    print >>out, '      <outline text="' + xml_escape(project.name) + '">'
    for task in tasks:
        print >>out, '        <outline text="' + xml_escape(task.name) + '" completed="' + task.date_completed.strftime (time_fmt) + '"/>'
    print >>out, '      </outline>'

def html_project_printer (out, project, tasks):
    time_fmt='%Y-%m-%d'
    print >>out, '    <H2>' + xml_escape(project.name) + '</H2>'
    print >>out, '    <P><UL>'
    for task in tasks:
        print >>out, '        <LI>' + xml_escape(task.name) + ' <font color="green"><i><small><b>' + task.date_completed.strftime (time_fmt) + '</b></small></i></font></LI>'
    print >>out, '    </UL></P>'
    
for arg in sys.argv[1:]:
    if arg[0] == '-':
        fmt = arg[1:]
    else:
        days = int(arg)

# Search Work folder and report on tasks completed in the last N days in the Log... context
# the number of days defaults to one but can be overridden on the command line

folders, contexts = build_model (find_database ())

file_name_base = os.environ['HOME']+'/Desktop/' + today.strftime (time_fmt)

# MARKDOWN
if fmt == 'md':
    file_name = file_name_base + '.md'
    out=codecs.open(file_name, 'w', 'utf-8')
    
    for folder in folders:
        if folder.name == 'Work':
            traverse_folder (DoneVisitor (out, include_completed_logged, md_project_printer), folder)

# FOLDING TEXT
elif fmt == 'ft':
    file_name = file_name_base + '.ft'
    out=codecs.open(file_name, 'w', 'utf-8')
    
    for folder in folders:
        if folder.name == 'Work':
            traverse_folder (DoneVisitor (out, include_completed_logged, ft_project_printer), folder)
            
# TASKPAPER            
elif fmt == 'tp':
    file_name = file_name_base + '.taskpaper'
    out=codecs.open(file_name, 'w', 'utf-8')

    for folder in folders:
        if folder.name == 'Work':
            traverse_folder (DoneVisitor (out, include_completed_logged, tp_project_printer), folder)
            
# MARKDOWN WEEKLY REPORT
elif fmt == 'week':
    days = 7
    file_name = file_name_base + '.taskpaper'
    out=codecs.open(file_name, 'w', 'utf-8')
    print >>out, 'Weekly Progress Report:'
    print >>out
    print >>out, '\tPaul Sidnell: ' + today.strftime ("%Y-%m-%d")
    print >>out
    print >>out, '\tAccomplishment For This Week:'
    
    # Search Work folder and report on tasks completed this year (I prune this context weekly - hence the name) in a Log... context
    for folder in folders:
        if folder.name == 'Work':
            traverse_folder (DoneVisitor (out, include_completed_logged, tp_weekly_project_printer), folder)
    
    print >>out, '\tPlans For Next Week:'
    print >>out, '\t\t- ?'
    print >>out, '\tComments/Issues:'
    
    for folder in folders:
        if folder.name == 'Work':
            traverse_folder (DoneVisitor (out, include_completed_logged, tp_weekly_project_printer), folder)
    print >>out, '\t\t- ?'

# OPML
elif fmt == 'opml':
    file_name = file_name_base + '.opml'
    out=codecs.open(file_name, 'w', 'utf-8')
    print >>out, '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
    print >>out, '<opml version="1.0">'
    print >>out, '  <head>'
    print >>out, '    <title>OmniFocus</title>'
    print >>out, '  </head>'
    print >>out, '  <body>'
    for folder in folders:
        if folder.name == 'Work':
            traverse_folder (DoneVisitor (out, include_completed_logged, opml_project_printer), folder)
    print >>out, '  </body>'
    print >>out, '</opml>'
    
# HTML
elif fmt == 'html':
    file_name = file_name_base + '.html'
    out=codecs.open(file_name, 'w', 'utf-8')
    print >>out, '<html>'
    print >>out, '  <head>'
    print >>out, '    <title>OmniFocus</title>'
    print >>out, '  </head>'
    print >>out, '  <body>'
    for folder in folders:
        if folder.name == 'Work':
            traverse_folder (DoneVisitor (out, include_completed_logged, html_project_printer), folder)
    print >>out, '  </body>'
    print >>out, '<html>'
else:
    raise Exception ('unknown format ' + fmt)


# Close the file and open it
out.close()
os.system("open '" + file_name + "'")
