import os
import codecs
import getopt
import sys
from treemodel import traverse_list
from omnifocus import build_model, find_database
from datetime import date
from of_to_tp import PrintTaskpaperVisitor
from of_to_text import PrintTextVisitor
from of_to_md import PrintMarkdownVisitor
from of_to_opml import PrintOpmlVisitor
from of_to_html import PrintHtmlVisitor
from visitors import FolderNameFilterVisitor, ProjectNameFilterVisitor, ContextNameFilterVisitor, TaskNameFilterVisitor, TaskCompletionFilterVisitor, ProjectCompletionFilterVisitor, TaskCompletionSortingVisitor, TaskFlaggedFilterVisitor, PruningFilterVisitor, FlatteningVisitor

VERSION = "1.0.0 (2013-04-09)" 
     
def print_structure (visitor, root_projects_and_folders, root_contexts, project_mode):
    if project_mode:
        traverse_list (visitor, root_projects_and_folders)
    else:
        traverse_list (visitor, root_contexts)

class CustomPrintTaskpaperVisitor (PrintTaskpaperVisitor):
    def tags (self, completed):
        if completed != None:
            return completed.strftime(" @%Y-%m-%d-%a")
        else:
            return ""
        
def print_help ():
    print 'Version ' + VERSION
    print 
    print 'Usage:'
    print
    print 'ofexport [options...] -o file_name'
    print
    print
    print 'options:'
    print '  -h,-?,--help'
    print '  -C: context mode (as opposed to project mode)'
    print '  -o file_name: the output file name, must end in a recognised suffix - see documentation'
    print '  --open: open the output file with the registered application (if one is installed)'
    print
    print 'filters:'
    print '  --pi regexp: include projects matching regexp'
    print '  --pe regexp: exclude projects matching regexp'
    print '  --fi regexp: include folders matching regexp'
    print '  --fe regexp: exclude folders matching regexp'
    print '  --ti regexp: include tasks matching regexp'
    print '  --te regexp: exclude tasks matching regexp'
    print '  --ci regexp: include contexts matching regexp'
    print '  --ce regexp: exclude contexts matching regexp'
    print '  --pci regexp: include projects with completion matching regexp'
    print '  --pce regexp: exclude projects with completion matching regexp'
    print '  --tci regexp: include tasks with completion matching regexp'
    print '  --tce regexp: exclude tasks with completion matching regexp'
    print '  --tfi: include flagged tasks'
    print '  --tfe: exclude flagged tasks'
    print '  --tsc: sort tasks by completion'
    print '  -F: flatten project/task structure'
    print '  --prune: prune empty projects or folders'

if __name__ == "__main__":
    
    today = date.today ()
    time_fmt='%Y-%m-%d'
    opn=False
    project_mode=True
    file_name = None
        
    opts, args = getopt.optlist, args = getopt.getopt(sys.argv[1:], 'hFC?o:',
                                                      ['fi=','fe=',
                                                       'pi=','pe=',
                                                       'ci=','ce=',
                                                       'pci=','pce=',
                                                       'ti=','te=',
                                                       'tci=','tce=',
                                                       'tfi','tfe',
                                                       'tsc',
                                                       'help',
                                                       'open',
                                                       'prune'])
    for opt, arg in opts:
        if '--open' == opt:
            opn = True
        elif '-C' == opt:
            project_mode = False
        elif '-o' == opt:
            file_name = arg;
        elif opt in ('-?', '-h', '--help'):
            print_help ()
            sys.exit()
    
    if file_name == None:
            print_help ()
            sys.exit()
    
    dot = file_name.index ('.')
    if dot == -1:
        print 'output file name must have suffix'
        sys.exit()
    
    fmt = file_name[dot+1:]
    
    root_projects_and_folders, root_contexts = build_model (find_database ())
    
    if project_mode:
        items = root_projects_and_folders
    else:
        items = root_contexts
        
    for opt, arg in opts:
        if '--fi' == opt:
            print 'include folders', arg
            traverse_list (FolderNameFilterVisitor (arg, include=True), items)
        elif '--fe' == opt:
            print 'exclude folders', arg
            traverse_list (FolderNameFilterVisitor (arg, include=False), items)
        elif '--pi' == opt:
            print 'include projects', arg
            traverse_list (ProjectNameFilterVisitor (arg, include=True), items)
        elif '--pe' == opt:
            print 'filter exclude projects', arg
            traverse_list (ProjectNameFilterVisitor (arg, include=False), items)
        elif '--ci' == opt:
            print 'contexts', arg
            traverse_list (ContextNameFilterVisitor (arg, include=True), items)
        elif '--ce' == opt:
            print 'contexts', arg
            traverse_list (ContextNameFilterVisitor (arg, include=False), items)
        elif '--ti' == opt:
            print 'include tasks', arg
            traverse_list (TaskNameFilterVisitor (arg, include=True), items)
        elif '--te' == opt:
            print 'exclude tasks', arg
            traverse_list (TaskNameFilterVisitor (arg, include=False), items)
        elif '--tci' == opt:
            print 'include task completion', arg
            traverse_list (TaskCompletionFilterVisitor (arg, include=True), items)
        elif '--tce' == opt:
            print 'include task completion', arg
            traverse_list (TaskCompletionFilterVisitor (arg, include=False), items)
        elif '--pci' == opt:
            print 'include project completion', arg
            traverse_list (ProjectCompletionFilterVisitor (arg, include=True), items)
        elif '--pce' == opt:
            print 'exclude project completion', arg
            traverse_list (ProjectCompletionFilterVisitor (arg, include=False), items)
        elif '--tfi' == opt:
            print 'include flagged tasks'
            traverse_list (TaskFlaggedFilterVisitor (include=True), items)
        elif '--tfe' == opt:
            print 'exclude flagged tasks'
            traverse_list (TaskFlaggedFilterVisitor (include=False), items)
        elif '--tsc' == opt:
            print 'sort by task completion'
            traverse_list (TaskCompletionSortingVisitor (), items)
        elif '--prune' == opt:
            print 'pruning empty folders, projects, contexts'
            traverse_list (PruningFilterVisitor (), items)
        elif '-F' == opt:
            visitor = FlatteningVisitor ()
            traverse_list (visitor, root_projects_and_folders)
            root_projects_and_folders = visitor.projects

    file_name_base = os.environ['HOME']+'/Desktop/'
    date_str = today.strftime (time_fmt)
    
    if fmt == 'txt' or fmt == 'text':
        out=codecs.open(file_name, 'w', 'utf-8')
        
        print_structure (PrintTextVisitor (out), root_projects_and_folders, root_contexts, project_mode)
        
    # MARKDOWN
    elif fmt == 'md' or fmt == 'markdown':
        out=codecs.open(file_name, 'w', 'utf-8')
        
        print_structure (PrintMarkdownVisitor (out), root_projects_and_folders, root_contexts, project_mode)
        
    # FOLDING TEXT
    elif fmt == 'ft' or fmt == 'foldingtext':
        out=codecs.open(file_name, 'w', 'utf-8')
        
        print_structure (PrintMarkdownVisitor (out), root_projects_and_folders, root_contexts, project_mode)
                
    # TASKPAPER            
    elif fmt == 'tp' or fmt == 'taskpaper':
        out=codecs.open(file_name, 'w', 'utf-8')

        print_structure (CustomPrintTaskpaperVisitor (out), root_projects_and_folders, root_contexts, project_mode)
    
    # OPML
    elif fmt == 'opml':
        out=codecs.open(file_name, 'w', 'utf-8')
        print >>out, '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        print >>out, '<opml version="1.0">'
        print >>out, '  <head>'
        print >>out, '    <title>OmniFocus</title>'
        print >>out, '  </head>'
        print >>out, '  <body>'
        
        print_structure (PrintOpmlVisitor (out, depth=1), root_projects_and_folders, root_contexts, project_mode)
        
        print >>out, '  </body>'
        print >>out, '</opml>'
        
    # HTML
    elif fmt == 'html' or fmt == 'htm':
        out=codecs.open(file_name, 'w', 'utf-8')
        print >>out, '<html>'
        print >>out, '  <head>'
        print >>out, '    <title>OmniFocus</title>'
        print >>out, '  </head>'
        print >>out, '  <body>'
        
        print_structure (PrintHtmlVisitor (out, depth=1), root_projects_and_folders, root_contexts, project_mode)
        
        print >>out, '  </body>'
        print >>out, '<html>'
    else:
        raise Exception ('unknown format ' + fmt)
    
    # Close the file and open it
    out.close()
    
    if opn:
        os.system("open '" + file_name + "'")
