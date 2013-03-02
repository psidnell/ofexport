from omnifocus import traverse_folder, build_model, DATABASE
from donereport import DoneReportVisitor, format_date
from datetime import date
import os
import codecs


days = 7
if len(os.sys.argv) > 1:
    days = int(os.sys.argv[1])

def completed_logged (task):
    if task.date_completed == None:
        return False
    if str(task.context).startswith('Log'):
        days_elapsed = (date.today() - task.date_completed).days
        return days_elapsed <= days
    return False

def completed_comments (task):
    if task.date_completed == None:
        return False
    if str(task.context).startswith('Comments'):
        days_elapsed = (date.today() - task.date_completed).days
        return days_elapsed <= days
    return False

folders, contexts = build_model (DATABASE)
file_name = os.environ['HOME']+'/Documents/Reports/WeeklyReport.tp'
out=codecs.open(file_name, 'w', 'utf-8')
print >>out, 'Weekly Progress Report:'
print >>out
print >>out, '\tPaul Sidnell: ' + format_date()
print >>out
print >>out, '\tAccomplishment For This Week:'
print >>out

# Search Work folder and report on tasks completed this year (I prune this context weekly - hence the name) in a Log... context
for folder in folders:
    if folder.name == 'Work':
        traverse_folder (DoneReportVisitor (out, completed_logged, proj_pfx='\t\t', proj_sfx=':', task_pfx='\t\t\t- ', time_fmt=' @%Y-%m-%d'), folder)

print >>out, '\tPlans For Next Week:'
print >>out
print >>out, '\tComments/Issues:'
print >>out

for folder in folders:
    if folder.name == 'Work':
        traverse_folder (DoneReportVisitor (out, completed_comments, proj_pfx='\t\t', proj_sfx=':', task_pfx='\t\t\t- ', time_fmt=' @%Y-%m-%d'), folder)

out.close()

os.system("open '" + file_name + "'")