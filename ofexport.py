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
from visitors import FolderNameFilterVisitor, ProjectNameFilterVisitor, ContextNameFilterVisitor, TaskNameFilterVisitor, TaskCompletionFilterVisitor, ProjectCompletionFilterVisitor, TaskCompletionSortingVisitor, PruningFilterVisitor, FlatteningVisitor
           
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
    print 'usage:'
    print 'ofexport [options...] -o file_name'
    print 'file_name: the output file name, must end in .tp, .taskpaper, .md, .html, or .opml'
    print
    print 'options:'
    print '  -h,-?,--help'
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
    print '  --tsc: sort tasks by completion'
    print '  -F: flatten project/task structure'
    print '  -C: context mode (as opposed to project mode)'
    print '  --prune: prune empty projects or folders'
    print '  --open: open the output file with the registered application (if one is installed)'
    print
    print 'examples:'
    print '  1. Create a taskpaper file containing everything in any folder called "Home" folder'
    print "    python ofexport.py --open -o ~/Desktop/OF.tp --fi '^Home$'"
    print '  2. Create a taskpaper file containing everything in any folder called "Home" or "Miscellaneous" folder'
    print "    python ofexport.py --open -o ~/Desktop/OF.tp --fi '^Home$|^Miscellaneous$'"
    print '  3. Create an opml file excluding everything in any folder called "Work"'
    print "    python ofexport.py --open -o ~/Desktop/OF.opml --fe '^Work$'"
    print '  4. Create a taskpaper file including everything in any folder called "Home", excluding completed items and excluding empty projects/folders'
    print "    python ofexport.py --open -o ~/Desktop/x.tp --fi '^Home$' --tce '.' --prune"
    print '  5. Create a taskpaper file including everything in any folder called "Home", including completed items from the last week'
    print "    python ofexport.py --open -o ~/Desktop/x.tp --fi '^Home$' --tci '-[0-6]d' --prune"
    print '  6. Create a taskpaper file including everything in any folder called "Home", including completed items from a specific day'
    print "    python ofexport.py --open -o ~/Desktop/x.tp --fi '^Home$' --tci '2013-02-10' --prune"
    print '  7. Create a taskpaper file including everything in any folder called "Home", including completed items from a February'
    print "    python ofexport.py --open -o ~/Desktop/x.tp --fi '^Home$' --tci 'Feb' --prune"
    print
    print "  The TODO.tp file was created with:"
    print "    python ofexport.py --open -o TODO.tp --pi OmniPythonLib --tce '.' --prune -F"
    print
    print "filtering:"
    print "  Filtering is based on regular expressions that match an items text. When an item is matched"
    print "  Then all it's direct ancestors to the root and all it's descendants are selected. If a single"
    print "  filter doesn't do quite what you want it's possible to provide several which are executed in order."
    print "  By using several inclusion/exclusion filters and fancy regular expressions it's possible to be very"
    print "  specific about what gets included in the final report." 
    print
    print "completion dates:"
    print "  Completion date matches are matched against a string of the form:"
    print "  '%Y-%m-%d %A %B' e.g. '2013-02-16 Saturday February -44d'"
    print "  This allows matches on day, date, how many days ago completion occurred or even days of the week."
    

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
            print 'project completion', arg
            traverse_list (ProjectCompletionFilterVisitor (arg, include=True), items)
        elif '--pce' == opt:
            print 'project completion', arg
            traverse_list (ProjectCompletionFilterVisitor (arg, include=False), items)
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
