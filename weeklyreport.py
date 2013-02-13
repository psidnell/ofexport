from omnifocus import traverse_folder, build_model
from donereport import DoneReportVisitor, format_date
from datetime import date
import os
import codecs

folders, contexts = build_model ('/Users/psidnell/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2')
file_name = '/Users/psidnell/Documents/Reports/WeeklyReport-' + date.today().strftime('%Y-%W') + '.md'
out=codecs.open(file_name, 'w', 'utf-8')
print >>out, '# Weekly Progress Report'
print >>out
print >>out, '## Paul Sidnell ' + format_date()
print >>out
print >>out, '---'
print >>out

# Search Work folder and report on tasks completed this year (I prune this context weekly - hence the name) in a Log... context
for folder in folders:
    if folder.name == 'Work':
        traverse_folder (DoneReportVisitor (out, proj_pfx='##', contextPrefix='Log', cmp_fmt='%Y'), folder)
out.close()

os.system("open '" + file_name + "'")