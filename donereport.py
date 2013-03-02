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
    
'''
This is a report visitor that looks for completed tasks in a context with a particular
prefix. At the end of each day I look at my completed tasks and set the context to Log
so that those tasks appear in my daily/weekly reports.
'''
class DoneReportVisitor(Visitor):

    def __init__ (self, out, inclusion_filter, proj_pfx='#', proj_sfx='', task_pfx='- ', time_fmt=' @%Y-%m-%d', indent=4):
        self.tasks = []
        self.out = out
        self.proj_pfx = proj_pfx
        self.proj_sfx = proj_sfx
        self.task_pfx = task_pfx
        self.time_fmt = time_fmt
        self.inclusion_filter = inclusion_filter
    def end_project (self, project):
        if len(self.tasks) > 0:
            print >>self.out, self.proj_pfx + ' ' + str(project) + self.proj_sfx
            self.tasks.sort(key=lambda task:task.date_completed)
            for task in self.tasks:
                print >>self.out, self.task_pfx + task.name + ' - ' + DAYS[task.date_completed.strftime('%w')] + ' ' + task.date_completed.strftime (self.time_fmt)
            print >>self.out
        self.tasks = []
    def begin_task (self, task):
        if self.inclusion_filter(task):
            self.tasks.append (task)
