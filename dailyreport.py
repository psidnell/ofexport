from omnifocus import traverse_folder, build_model
from donereport import DoneReportVisitor, format_timestamp
import os
import codecs


folders, contexts = build_model ('/Users/psidnell/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2')

file_name='/Users/psidnell/Documents/Reports/DailyReport-' + format_timestamp () + '.md'
out=codecs.open(file_name, 'w', 'utf-8')

# Search Work folder and report on tasks completed today in a Log... context
for folder in folders:
    if folder.name == 'Work':
        traverse_folder (DoneReportVisitor (out, proj_pfx='#', contextPrefix='Log', cmp_fmt='%Y%j'), folder)
out.close()
os.system("open '" + file_name + "'")