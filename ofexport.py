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

import os
import re
import codecs
import getopt
import sys
import json
from datetime import datetime
from datematch import process_date_specifier, date_range_to_str, match_date_against_range
from treemodel import traverse, traverse_list, PROJECT, TASK, FOLDER, CONTEXT
from omnifocus import build_model, find_database
from datetime import date
from of_to_tp import PrintTaskpaperVisitor
from of_to_text import PrintTextVisitor
from of_to_md import PrintMarkdownVisitor
from of_to_opml import PrintOpmlVisitor
from of_to_html import PrintHtmlVisitor
from of_to_json import ConvertStructureToJsonVisitor
from visitors import Filter, Sort, Prune, Flatten

VERSION = "1.0.5 (2013-04-18)"

NAME_ALIASES = ['title', 'text', 'name', '']
START_ALIASES = ['start', 'started', 'begin', 'began']
COMPLETED_ALIASES = ['done', 'end', 'ended', 'complete', 'completed', 'finish', 'finished', 'completion']
DUE_ALIASES = ['due', 'deadline']
FLAGGED_ALIASES = ['flag', 'flagged']

def get_date_attrib_or_now (item, attrib):
    if not attrib in item.__dict__:
        return datetime.now()
    result = item.__dict__[attrib]
    if result == None:
        return datetime.now()
    return result

def build_filter (item_types, include, field, arg):
    if 'prune' == field:
        item_types = [x for x in item_types if x in [PROJECT, CONTEXT, FOLDER]]
        return Prune (item_types)
    elif 'flatten' == field:
        return Flatten (item_types)
    elif 'sort' == field:
        if arg == None or arg in NAME_ALIASES:
            get_name = lambda x: x.name
            return Sort (item_types, get_name, 'text')
        elif arg in START_ALIASES:
            item_types = [x for x in item_types if x in [TASK, PROJECT]]
            get_start = lambda x: get_date_attrib_or_now (x, 'start')
            return Sort (item_types, get_start, 'start')
        elif arg in COMPLETED_ALIASES:
            item_types = [x for x in item_types if x in [TASK, PROJECT]]
            get_completion = lambda x: get_date_attrib_or_now (x, 'date_completed')
            return Sort (item_types, get_completion, 'completion')
        elif arg in DUE_ALIASES:
            item_types = [x for x in item_types if x in [TASK, PROJECT]]
            get_due = lambda x: get_date_attrib_or_now (x, 'due')
            return Sort (item_types, get_due, 'due')
        elif arg in FLAGGED_ALIASES:
            item_types = [x for x in item_types if x in [TASK, PROJECT]]
            get_not_flagged = lambda x: not x.flagged
            return Sort (item_types, get_not_flagged, 'flagged')
        else:
            assert False, 'unsupported field: ' + field
    else:
        if field in NAME_ALIASES:
            nice_str = NAME_ALIASES[0] + ' = ' + arg
            match_name = lambda item, regexp: re.search (regexp, item.name) != None
            return Filter (item_types, match_name, arg, include, nice_str)
        elif field in START_ALIASES:
            item_types = [x for x in item_types if x in [TASK, PROJECT]]
            rng = process_date_specifier (datetime.now(), arg)
            nice_str = START_ALIASES[0] + ' = ' + date_range_to_str (rng)
            match_start = lambda x, r: match_date_against_range (x.date_to_start, r)
            return Filter (item_types, match_start, rng, include, nice_str)
        elif field in COMPLETED_ALIASES:
            item_types = [x for x in item_types if x in [TASK, PROJECT]]
            rng = process_date_specifier (datetime.now(), arg)
            nice_str = COMPLETED_ALIASES[0] + ' = ' + date_range_to_str (rng)
            match_completed = lambda x, r: match_date_against_range (x.date_completed, r)
            return Filter (item_types, match_completed, rng, include, nice_str)
        elif field in DUE_ALIASES:
            item_types = [x for x in item_types if x in [TASK, PROJECT]]
            rng = process_date_specifier (datetime.now(), arg)
            nice_str = DUE_ALIASES[0] + ' = ' + date_range_to_str (rng)
            match_due = lambda x, r: match_date_against_range (x.date_due, r)
            return Filter (item_types, match_due, rng, include, nice_str)
        elif field in FLAGGED_ALIASES:
            item_types = [x for x in item_types if x in [TASK, PROJECT]]
            match_flagged = lambda x, ignore: x.flagged
            return Filter (item_types, match_flagged, None, include, field)
        else:
            assert False, 'unsupported field: ' + field
    
    
def parse_command (param):
    if param.startswith ('flag'):
        return (True, 'flagged', None)
    elif param.startswith ('!flag'):
        return (False, 'flagged', None)
    elif param =='prune':
        return (True, 'prune', None)
    elif param == 'sort':
        return (True, 'sort', None)
    elif param.startswith('flat'):
        return (True, 'flatten', None)
    
    params = param.split('=', 1)
    assert len(params) == 2
    # We've got x=y or x!=y
    include = True
    if params[0].endswith ('!'):
        include = False
        field=params[0][:-1]
        value=params[1]
    else:
        field=params[0]
        value=params[1]
    return (include, field, value)
    
    
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


class CustomPrintTaskpaperVisitor (PrintTaskpaperVisitor):
    def __init__(self, out, links=False):
        PrintTaskpaperVisitor.__init__(self, out, links=links)
    def tags (self, item):
        if item.date_completed != None and item.type != PROJECT:
            return item.date_completed.strftime(" @%Y-%m-%d-%a")
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
    print '  -P: project mode - the default (as opposed to context mode)'
    print '  -l: print links to tasks (in supported file formats)'
    print '  -o file_name: the output file name, must end in a recognised suffix - see documentation'
    print '  --open: open the output file with the registered application (if one is installed)'
    print
    print 'filters:'
    print '  -a,--any     filter tasks, projects, contexts and folders against argument'
    print '  -t,--task    filter any task against task against argument'
    print '  -p,--project filter any project against argument'
    print '  -f,--folder  filter any folder against argument'
    print '  -c,--context filter any context type against argument'
    print 
    print '  A filter argument may be:'
    print '    text=regexp'
    print '    text!=regexp'
    print '    =regexp (abbrieviation of text=regexp)'
    print '    !=regexp (abbrieviation of text!=regexp)'
    print '    flagged'
    print '    !flagged'
    print '    due=tomorrow'
    print '    start!=this week (this will need quoting on the command line, because of the space)'
    print '    sort=completed'
    print '    prune'
    print '    flatten'
    print
    print '  See DOCUMENTATION.md for more information'

if __name__ == "__main__":
    
    today = date.today ()
    time_fmt='%Y-%m-%d'
    opn=False
    project_mode=True
    file_name = None
    paul = False
    links = False
        
    opts, args = getopt.optlist, args = getopt.getopt(sys.argv[1:],
                'p:c:t:f:a:hlCP?o:',
                ['project=',
                 'context=',
                 'task=',
                 'folder=',
                 'any=',
                 'help',
                 'open',
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
            included, field, arg = parse_command (arg)
            visitor = build_filter ([PROJECT], included, field, arg)
        elif opt in ('--task', '-t'):
            included, field, arg = parse_command (arg)
            visitor = build_filter ([TASK], included, field, arg)
        elif opt in ('--context', '-c'):
            included, field, arg = parse_command (arg)
            visitor = build_filter ([CONTEXT], included, field, arg)
        elif opt in ('--folder', '-f'):
            included, field, arg = parse_command (arg)
            visitor = build_filter ([FOLDER], included, field, arg)
        elif opt in ('--any', '-a'):
            included, field, arg = parse_command (arg)
            visitor = build_filter ([TASK,PROJECT,FOLDER,CONTEXT], included, field, arg)
        elif '-C' == opt:
            subject = root_context
        elif '-P' == opt:
            subject = root_project
        
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
        
        visitor = PrintHtmlVisitor (out, depth=1)
        traverse_list (visitor, subject.children, project_mode=project_mode)       
        
        print >>out, '  </body>'
        print >>out, '<html>'
    # HTML
    elif fmt == 'json':
        out=codecs.open(file_name, 'w', 'utf-8')
        
        visitor = ConvertStructureToJsonVisitor ()
        traverse (visitor, root_project, project_mode=True)
        
        visitor = ConvertStructureToJsonVisitor ()
        traverse (visitor, root_context, project_mode=False)
        
        print >> out, json.dumps([root_project.attribs['json_data'], root_context.attribs['json_data']], indent=4)
    else:
        raise Exception ('unknown format ' + fmt)
    
    # Close the file and open it
    out.close()
    
    if opn:
        os.system("open '" + file_name + "'")
