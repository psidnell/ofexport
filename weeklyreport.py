import omnifocus
from datetime import date
import os

folders, contexts = omnifocus.buildModel ('/Users/psidnell/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2')
file_name = '/Users/psidnell/Documents/Reports/WeeklyReport-' + date.today().strftime('%W') + '.ft'
out=open(file_name, 'w')
print >>out, '# Weekly Progress Report'
print >>out
print >>out, '## Paul Sidnell ' + omnifocus.format_date()
print >>out
print >>out, '---'
print >>out

for folder in folders:
    if folder.name == 'Work':
        omnifocus.traverse_folder (omnifocus.WeeklyReportVisitor (out, proj_pfx='##', days=7), folder)
out.close()

os.system("open '" + file_name + "'")