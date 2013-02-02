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
    
class WeeklyReportVisitor(Visitor):

    def __init__ (self, out, proj_pfx='#', cmp_fmt='%Y%W', indent=4):
        self.cmp_fmt = cmp_fmt
        self.tasks = []
        self.out = out
        self.proj_pfx = proj_pfx
    def end_project (self, project):
        if len(self.tasks) > 0 or self.completed_recently(project):
            print >>self.out, self.proj_pfx + ' ' + str(project)
            self.tasks.sort(key=lambda task:task.date_completed)
            for task in self.tasks:
                print >>self.out, '- ' + task.name + ' *[' + format_date(task.date_completed) + ']*'
            if project.date_completed != None:
                print >>self.out, '- Finished *[' + format_date(project.date_completed) + ']*'
            print >>self.out
        self.tasks = []
    def begin_task (self, task):
        if self.completed_recently(task) and str(task.context).startswith('Log'):
            self.tasks.append (task)
    def completed_recently (self, task):
        if task.date_completed == None:
            return False
        return task.date_completed.strftime(self.cmp_fmt) == date.today().strftime(self.cmp_fmt)
