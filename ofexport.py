'''
Copyright 2013 Paul Sidnell

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from datetime import datetime
from datematch import process_date_specifier, date_range_to_str
import os
import codecs
import getopt
import sys
from treemodel import traverse, traverse_list, PROJECT, TASK, FOLDER, CONTEXT
from omnifocus import build_model, find_database
from datetime import date
from of_to_tp import PrintTaskpaperVisitor
from of_to_text import PrintTextVisitor
from of_to_md import PrintMarkdownVisitor
from of_to_opml import PrintOpmlVisitor
from of_to_html import PrintHtmlVisitor
from visitors import Filter, Sort, match_name, match_start, match_completed, match_due, match_flagged, get_name, get_start, get_due, get_completion, PruningFilterVisitor, FlatteningVisitor

VERSION = "1.0.4 (2013-04-15)" 

class CustomPrintTaskpaperVisitor (PrintTaskpaperVisitor):
    def __init__(self, out, links=False):
        PrintTaskpaperVisitor.__init__(self, out, links=links)
    def tags (self, item):
        if item.date_completed != None and item.type != PROJECT:
            return item.date_completed.strftime(" @%Y-%m-%d-%a")
        else:
            return ""
    
def build_filter (item_types, instruction, field, arg):
    if 'include'.startswith(instruction) or 'exclude'.startswith (instruction):
        include = 'include'.startswith (instruction)
        if field in ('title', 'text'):
            return Filter (item_types, match_name, arg, include, field + ':' + arg)
        if field in ('start', 'started', 'begin', 'began'):
            rng = process_date_specifier (datetime.now(), arg)
            nice_str = date_range_to_str (rng)
            return Filter (item_types, match_start, rng, include, nice_str)
        if field in ('end', 'ended', 'complete', 'completed', 'finish', 'finished', 'completion'):
            rng = process_date_specifier (datetime.now(), arg)
            nice_str = date_range_to_str (rng)
            return Filter (item_types, match_completed, rng, include, nice_str)
        if field in ('due', 'deadline'):
            rng = process_date_specifier (datetime.now(), arg)
            nice_str = date_range_to_str (rng)
            return Filter (item_types, match_due, rng, include, nice_str)
        if field in ('flag', 'flagged'):
            return Filter (item_types, match_flagged, None, include, field)
        else:
            assert False, 'unsupported field: ' + field
    elif 'sort'.startswith (instruction):
        if field in ('title', 'text'):
            return Sort (item_types, get_name, 'text')
        if field in ('start', 'started', 'begin', 'began'):
            return Sort (item_types, get_start, 'start')
        if field in ('end', 'ended', 'complete', 'completed', 'finish', 'finished', 'completion'):
            return Sort (item_types, get_completion, 'complete')
        if field in ('due', 'deadline'):
            return Sort (item_types, get_due, 'due')
        else:
            assert False, 'unsupported field: ' + field
    
def parse_command (param):
    #param = p1[:p2[:p3]]
    params = param.split(':', 2)
    instruction = params[0]
    field = None
    arg = None
    if 'include'.startswith(instruction) or 'exclude'.startswith (instruction):
        assert 'command invalid: ' + param, len (params>=2)
        field = params[1]
        arg = None
        if not 'flagged'.startswith(field):
            assert 'command invalid: ' + param, len (params==3)
            arg = params[2]
    elif 'sort'.startswith (instruction):
        assert 'command invalid: ' + param, len (params==2)
        field = params[1]
    else:
        assert False, 'command invalid: ' + param
    return (instruction, field, arg)
       
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
    print '  -P: project mode - the default (as opposed to context mode)'
    print '  -l: print links to tasks (in supported file formats)'
    print '  -o file_name: the output file name, must end in a recognised suffix - see documentation'
    print '  --open: open the output file with the registered application (if one is installed)'
    print
    print 'filters:'
    
    print '  -i regexp: include anything matching regexp'
    print '  -e regexp: exclude anything matching regexp'
    
    print '  --si spec: include anything with start matching spec'
    print '  --se spec: exclude anything with start matching spec'
    
    print '  --di spec: include anything with due matching spec'
    print '  --de spec: exclude anything with due matching spec'
    
    print '  --ci spec: include anything with completion matching spec'
    print '  --ce spec: exclude anything with completion matching spec'
    
    print '  --Fi regexp: include anything flagged'
    print '  --Fe regexp: exclude anything flagged'
    
    print '  --pi regexp: include projects matching regexp'
    print '  --pe regexp: exclude projects matching regexp'
    
    print '  --pci spec: include projects with completion matching spec'
    print '  --pce spec: exclude projects with completion matching spec'
    
    print '  --pdi spec: include projects with due matching spec'
    print '  --pde spec: exclude projects with due matching spec'
    
    print '  --psi spec: include projects with start matching spec'
    print '  --pse spec: exclude projects with start matching spec'
    
    print '  --pfi: include flagged projects'
    print '  --pfe: exclude flagged projects'
    
    print '  --fi regexp: include folders matching regexp'
    print '  --fe regexp: exclude folders matching regexp'
    
    print '  --ti regexp: include tasks matching regexp'
    print '  --te regexp: exclude tasks matching regexp'
    
    print '  --Ci regexp: include contexts matching regexp'
    print '  --Ce regexp: exclude contexts matching regexp'
     
    print '  --tci spec: include tasks with completion matching spec'
    print '  --tce spec: exclude tasks with completion matching spec'
    
    print '  --tsi spec: include tasks with start matching spec'
    print '  --tse spec: exclude tasks with start matching spec'
    
    print '  --tdi spec: include tasks with due matching spec'
    print '  --tde spec: exclude tasks with due matching spec'
    
    print '  --tfi: include flagged tasks'
    print '  --tfe: exclude flagged tasks'
    
    print '  --tsc: sort tasks by completion'
    print '  --fsa: sort folders/projects alphabetically'
    print '  --csa: sort contexts alphabetically'
    print '  --sa: sort everything alphabetically'
    
    print '  -F: flatten project/task structure'
    print '  --prune: prune empty projects or folders'

if __name__ == "__main__":
    
    today = date.today ()
    time_fmt='%Y-%m-%d'
    opn=False
    project_mode=True
    file_name = None
    paul = False
    links = False
        
    opts, args = getopt.optlist, args = getopt.getopt(sys.argv[1:],
                'p:c:t:f:a:hlFC?o:',
                ['project=',
                 'context=',
                 'task=',
                 'folder=',
                 'any=',
                 'help',
                 'open',
                 'prune',
                 'paul'])
    for opt, arg in opts:
        if '--open' == opt:
            opn = True
        elif '--paul' == opt:
            paul = True
        elif '-l' == opt:
            links = True
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
    
    root_project, root_context = build_model (find_database ())
    subject = root_project
        
    for opt, arg in opts:
        visitor = None
        if opt in ('--project', '-p'):
            instruction, field, arg = parse_command (arg)
            visitor = build_filter ([PROJECT], instruction, field, arg)
        elif opt in ('--task', '-t'):
            instruction, field, arg = parse_command (arg)
            visitor = build_filter ([TASK], instruction, field, arg)
        elif opt in ('--context', '-c'):
            instruction, field, arg = parse_command (arg)
            visitor = build_filter ([CONTEXT], instruction, field, arg)
        elif opt in ('--folder', '-f'):
            instruction, field, arg = parse_command (arg)
            print instruction, field, arg
            visitor = build_filter ([FOLDER], instruction, field, arg)
        elif opt in ('--any', '-a'):
            instruction, field, arg = parse_command (arg)
            visitor = build_filter ([TASK,PROJECT,FOLDER,CONTEXT], instruction, field, arg)
        elif '--prune' == opt:
            visitor = PruningFilterVisitor ()
        elif '-F' == opt:
            visitor = FlatteningVisitor ()
        
        if visitor != None: 
            print str (visitor)
            traverse (visitor, subject, project_mode=project_mode)
                    
    print 'Generating', file_name
    
    out=codecs.open(file_name, 'w', 'utf-8')
    
    if fmt == 'txt' or fmt == 'text':        
        visitor = PrintTextVisitor (out)
        traverse_list (visitor, subject.children, project_mode=project_mode)       
    elif fmt == 'md' or fmt == 'markdown':
        visitor = PrintMarkdownVisitor (out)
        traverse_list (visitor, subject.children, project_mode=project_mode)       
    elif fmt == 'ft' or fmt == 'foldingtext':        
        visitor = PrintMarkdownVisitor (out)
        traverse_list (visitor, subject.children, project_mode=project_mode)       
    elif fmt == 'tp' or fmt == 'taskpaper':
        if paul:
            visitor = CustomPrintTaskpaperVisitor (out, links=links)
        else:
            visitor = PrintTaskpaperVisitor (out, links = links)
        traverse_list (visitor, subject.children, project_mode=project_mode)       
    elif fmt == 'opml':
        print >>out, '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        print >>out, '<opml version="1.0">'
        print >>out, '  <head>'
        print >>out, '    <title>OmniFocus</title>'
        print >>out, '  </head>'
        print >>out, '  <body>'
        
        visitor = PrintOpmlVisitor (out, depth=1)
        traverse_list (visitor, subject.children, project_mode=project_mode)       
        
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
        
        visitor - PrintHtmlVisitor (out, depth=1)
        traverse_list (visitor, subject.children, project_mode=project_mode)       
        
        print >>out, '  </body>'
        print >>out, '<html>'
    else:
        raise Exception ('unknown format ' + fmt)
    
    # Close the file and open it
    out.close()
    
    if opn:
        os.system("open '" + file_name + "'")
