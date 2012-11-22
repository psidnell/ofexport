from omnifocus import Visitor, build_model, traverse_folder
from datetime import date
import os
import codecs

DAYS={'0':'Sun', '1':'Mon', '2':'Tue', '3':'Wed', '4':'Thu', '5':'Fri', '6':'Sat'}
MONTHS={'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul','08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}

def format_date (thedate = date.today()):
        if thedate == None:
            return ''
        result = DAYS[thedate.strftime('%w')]
        result += ' ' + MONTHS[thedate.strftime('%m')]
        result += thedate.strftime(' %d %Y')
        return result
    
def format_timestamp (thedate = date.today()):
        return thedate.strftime('%Y-%m-%d')
    
class WeeklyReportVisitor(Visitor):

    def __init__ (self, out, proj_pfx='#', indent=4):
        self.tasks_todo = []
        self.tasks_done = []
        self.out = out
        self.proj_pfx = proj_pfx
    def end_project (self, project):
        if len(self.tasks_todo) > 0 and project.date_completed == None and project.name.startswith ('CONSER'):
            print >>self.out, self.proj_pfx + ' ' + project.name
            self.tasks_done.sort(key=lambda task:task.rank)
            self.tasks_done.sort(key=lambda task:task.date_completed)
            for task in self.tasks_todo:
                print >>self.out, '- ' + task.name
            for task in self.tasks_done:
                print >>self.out, '- ' + task.name + ' *[' + format_date(task.date_completed) + ']*'
            if project.date_completed != None:
                print >>self.out, '- Finished *[' + format_date(project.date_completed) + ']*'
            print >>self.out
        self.tasks_todo = []
        self.tasks_done = []
    def begin_task (self, task):
        if task.date_completed == None:
            self.tasks_todo.append (task)
        else:
            self.tasks_done.append (task)

    
folders, contexts = build_model ('/Users/psidnell/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2')

file_name='/Users/psidnell/Documents/Reports/ConserReport.md'
out=codecs.open(file_name, 'w', 'utf-8')
for folder in folders:
    if folder.name == 'Work':
        traverse_folder (WeeklyReportVisitor (out, proj_pfx='#'), folder)
out.close()
os.system("open '" + file_name + "'")
