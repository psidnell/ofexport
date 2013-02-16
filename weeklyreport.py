from omnifocus import traverse_folder, build_model, DATABASE
from donereport import DoneReportVisitor, format_date
from datetime import date
import os
import codecs

def completed_recently (task):
    if task.date_completed == None:
        return False
    days_elapsed = (date.today() - task.date_completed).days
    return days_elapsed <= 7

folders, contexts = build_model (DATABASE)
file_name = os.environ['HOME']+'/Documents/Reports/WeeklyReport-' + date.today().strftime('%Y-%W') + '.md'
out=codecs.open(file_name, 'w', 'utf-8')
print >>out, '# Weekly Progress Report'
print >>out
print >>out, '## Paul Sidnell ' + format_date()
print >>out
print >>out, '---'
print >>out
print >>out, '# Accomplishment For This Week'
print >>out

# Search Work folder and report on tasks completed this year (I prune this context weekly - hence the name) in a Log... context
for folder in folders:
    if folder.name == 'Work':
        traverse_folder (DoneReportVisitor (out, completed_recently, proj_pfx='##', contextPrefix='Log'), folder)

print >>out, '# Plans For Next Week'
print >>out
print >>out, '# Comments/Issues'
print >>out
out.close()

os.system("open '" + file_name + "'")