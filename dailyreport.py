from omnifocus import traverse_folder, build_model
from donereport import WeeklyReportVisitor, format_timestamp
import os

folders, contexts = build_model ('/Users/psidnell/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2')

file_name='/Users/psidnell/Documents/Reports/DailyReport-' + format_timestamp () + '.ft'
out=open(file_name, 'w')
for folder in folders:
    if folder.name == 'Work':
        traverse_folder (WeeklyReportVisitor (out, proj_pfx='#', cmp_fmt='%Y%j'), folder)
out.close()
os.system("open '" + file_name + "'")