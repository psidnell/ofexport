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
from treemodel import traverse, traverse_list, Visitor, PROJECT, TASK, FOLDER, CONTEXT
from omnifocus import build_model, find_database
from datetime import date
from of_to_tp import PrintTaskpaperVisitor
from of_to_text import PrintTextVisitor
from of_to_md import PrintMarkdownVisitor
from of_to_opml import PrintOpmlVisitor
from of_to_html import PrintHtmlVisitor
from of_to_json import ConvertStructureToJsonVisitor, read_json
from visitors import Filter, Sort, Prune, Flatten
from help import print_help, SHORT_OPTS, LONG_OPTS
from fmt_template import FmtTemplate, format_document
from cmd_parser import make_filter, NAME_ALIASES, START_ALIASES, COMPLETED_ALIASES, DUE_ALIASES, FLAGGED_ALIASES, FLATTEN_ALIASES

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
            match_name = lambda item, regexp: re.compile (arg).search (item.name) != None
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
        elif field =='flagged_or_due':
            item_types = [x for x in item_types if x in [TASK, PROJECT]]
            rng = process_date_specifier (datetime.now(), arg)
            nice_str = DUE_ALIASES[0] + ' = ' + date_range_to_str (rng)
            match_due = lambda x, r: match_date_against_range (x.date_due, r) or x.flagged
            return Filter (item_types, match_due, rng, include, nice_str)
        else:
            assert False, 'unsupported field: ' + field

class SummaryVisitor (Visitor):
    def __init__ (self):
        self.counts = {}
    def end_any (self, item):
        if not 'counted' in item.attribs:
            item.attribs['counted'] = True
            if item.type in self.counts:
                self.counts[item.type] = self.counts[item.type] + 1
            else:
                self.counts[item.type] = 1
    def print_counts (self):
        # Subtract for the extra invisible roots that we've added.
        if CONTEXT in self.counts:
            self.counts[CONTEXT] = self.counts[CONTEXT]-1
        if FOLDER in self.counts:
            self.counts[FOLDER] = self.counts[FOLDER]-1
        
        print 'Report Contents:'
        print '----------------'
        for k,v in [(k,self.counts[k]) for k in sorted(self.counts.keys())]:
            k = ' ' * (8 - len(k)) + k + 's:'
            print k, v
        print '----------------'
    
def parse_command (param):
    if param in FLAGGED_ALIASES:
        return (True, 'flagged', None)
    elif param.startswith ('!') and param[1:] in FLAGGED_ALIASES:
        return (False, 'flagged', None)
    elif param =='prune':
        return (True, 'prune', None)
    elif param == 'sort':
        return (True, 'sort', None)
    elif param in FLATTEN_ALIASES:
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


def load_template (template_dir, name):
    print 'loading template: ' + name
    instream=codecs.open(template_dir + name + '.json', 'r', 'utf-8')
    template = FmtTemplate (json.loads(instream.read()))
    instream.close ()
    return template

if __name__ == "__main__":
    
    today = date.today ()
    time_fmt='%Y-%m-%d'
    opn=False
    project_mode=True
    file_name = None
    infile = None
    template = None
    template_dir = os.environ['OFEXPORT_HOME'] + '/templates/'
    
    opts, args = getopt.optlist, args = getopt.getopt(sys.argv[1:],SHORT_OPTS, LONG_OPTS)
              
    for opt, arg in opts:
        if '--open' == opt:
            opn = True
        elif '-o' == opt:
            file_name = arg
        elif '-i' == opt:
            infile = arg;
        elif '-T' == opt:
            template = load_template (template_dir, arg)
        elif opt in ('-?', '-h', '--help'):
            print_help ()
            sys.exit()
    
    if file_name == None:
            print_help ()
            sys.exit()
    
    
    if file_name.find ('.') == -1:
        print 'output file name must have suffix: ' + file_name
        sys.exit()
    dot = file_name.index ('.')
    fmt = file_name[dot+1:]
    
    if infile != None:
        root_project, root_context = read_json (infile)
    else:    
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
        elif opt in ('--expression', '-e'):
            visitor = make_filter (arg)
        elif '-C' == opt:
            subject = root_context
        elif '-P' == opt:
            subject = root_project
        
        if visitor != None: 
            print str (visitor)
            traverse_list (visitor, subject.children, project_mode=project_mode)
                    
    print 'Generating', file_name
    
    out=codecs.open(file_name, 'w', 'utf-8')
    
    if fmt in ('txt', 'text'):
        template = template if template != None else load_template (template_dir, 'text')
        visitor = PrintTextVisitor (out, template)
        format_document (subject, visitor, project_mode)
    elif fmt in ('md', 'markdown', 'ft', 'foldingtext'):
        template = template if template != None else load_template (template_dir, 'markdown')
        visitor = PrintMarkdownVisitor (out, template)
        format_document (subject, visitor, project_mode)
    elif fmt in ('tp', 'taskpaper'):
        template = template if template != None else load_template (template_dir, 'taskpaper')
        visitor = PrintTaskpaperVisitor (out, template)
        format_document (subject, visitor, project_mode)
    elif fmt == 'opml':
        template = template if template != None else load_template (template_dir, 'opml')
        visitor = PrintOpmlVisitor (out, template)
        format_document (subject, visitor, project_mode)
    elif fmt in ('html', 'htm'):
        template = template if template != None else load_template (template_dir, 'html')
        visitor = PrintHtmlVisitor (out, template)
        format_document (subject, visitor, project_mode)
    elif fmt == 'json':
        # json has intrinsic formatting - no template required
        root_project.marked = True
        root_context.marked = True
        visitor = ConvertStructureToJsonVisitor ()
        traverse (visitor, root_project, project_mode=True)
        visitor = ConvertStructureToJsonVisitor ()
        traverse (visitor, root_context, project_mode=False)
        print >> out, json.dumps([root_project.attribs['json_data'], root_context.attribs['json_data']], sort_keys=True, indent=2)
    else:
        raise Exception ('unknown format ' + fmt)
    
    # Close the file and open it
    out.close()
    
    if opn:
        os.system("open '" + file_name + "'")
        
    visitor = SummaryVisitor ()
    traverse (visitor, root_project, project_mode=True)
    traverse (visitor, root_context, project_mode=False)
    visitor.print_counts()
