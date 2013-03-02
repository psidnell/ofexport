from omnifocus import traverse_folder, build_model, DATABASE
from donereport import DoneReportVisitor
import os
import codecs
from datetime import date
import sys

folders, contexts = build_model (DATABASE)

file_name=os.environ['HOME'] + '/Dropbox/TaskPaper/Work/DailyReport.taskpaper'
out=codecs.open(file_name, 'w', 'utf-8')

cmp_fmt='%Y%j'

days = 1
if len(sys.argv) > 1:
    days = int(sys.argv[1])

def include_completed_logged (task):
    if task.date_completed == None:
        return False
    if str(task.context).startswith('Log') or str(task.context).startswith('Comments'):
        days_elapsed = (date.today() - task.date_completed).days
        return days_elapsed < days
    return False

# Search Work folder and report on tasks completed in the last N days in the Log... context
# the number of days defaults to one but can be overridden on the command line
for folder in folders:
    if folder.name == 'Work':
        traverse_folder (DoneReportVisitor (out, include_completed_logged, proj_pfx='', proj_sfx=':', task_pfx='\t\t- '), folder)
        
out.close()
os.system("open '" + file_name + "'")
