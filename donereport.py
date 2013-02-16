from omnifocus import Visitor
from datetime import date

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
    
'''
This is a report visitor that looks for completed tasks in a context with a particular
prefix. At the end of each day I look at my completed tasks and set the context to Log
so that those tasks appear in my daily/weekly reports.
'''
class DoneReportVisitor(Visitor):

    def __init__ (self, out, date_filter, proj_pfx='#', contextPrefix='Log', indent=4):
        self.tasks = []
        self.out = out
        self.contextPrefix = contextPrefix
        self.proj_pfx = proj_pfx
        self.date_filter = date_filter
    def end_project (self, project):
        if len(self.tasks) > 0:
            print >>self.out, self.proj_pfx + ' ' + str(project)
            self.tasks.sort(key=lambda task:task.date_completed)
            for task in self.tasks:
                print >>self.out, '- ' + task.name + ' *[' + format_date(task.date_completed) + ']*'
            print >>self.out
        self.tasks = []
    def begin_task (self, task):
        if self.date_filter(task) and str(task.context).startswith(self.contextPrefix):
            self.tasks.append (task)
