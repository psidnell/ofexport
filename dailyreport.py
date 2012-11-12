import omnifocus
from datetime import date
import os

folders, contexts = omnifocus.buildModel ('/Users/psidnell/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2')

file_name='/Users/psidnell/Documents/Reports/DailyReport-' + omnifocus.format_timestamp () + '.ft'
out=open(file_name, 'w')
for folder in folders:
    if folder.name == 'Work':
        omnifocus.traverse_folder (omnifocus.WeeklyReportVisitor (out, proj_pfx='#', days=1), folder)
out.close()
os.system("open '" + file_name + "'")