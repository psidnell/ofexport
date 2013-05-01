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
import codecs
import getopt
import sys
import json
from treemodel import traverse, Visitor, FOLDER, CONTEXT, PROJECT, TASK
from omnifocus import build_model, find_database
from datetime import date, datetime
from of_to_tp import PrintTaskpaperVisitor
from of_to_text import PrintTextVisitor
from of_to_md import PrintMarkdownVisitor
from of_to_opml import PrintOpmlVisitor
from of_to_html import PrintHtmlVisitor
from of_to_json import ConvertStructureToJsonVisitor, read_json
from help import print_help, SHORT_OPTS, LONG_OPTS
from fmt_template import FmtTemplate, format_document
from cmd_parser import make_filter
import logging
import cmd_parser

logging.basicConfig(format='%(asctime)-15s %(name)s %(levelname)s %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.ERROR)

LOGGER_NAMES = [
                __name__,
                'cmd_parser',
                'visitors',
                'datematch',
                'treemodel',
                'omnifocus']

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
        
        logger.info ('Report Contents:')
        logger.info ('----------------')
        for k,v in [(k,self.counts[k]) for k in sorted(self.counts.keys())]:
            k = ' ' * (8 - len(k)) + k + 's:'
            logger.info (k + ' ' + str(v))
        logger.info ('----------------')

def load_template (template_dir, name):
    logger.info ('loading template: %s', name)
    instream=codecs.open(template_dir + name + '.json', 'r', 'utf-8')
    template = FmtTemplate (json.loads(instream.read()))
    instream.close ()
    return template

def fix_abbrieviated_expr (typ, arg):
    if arg.startswith ('=') or arg.startswith ('!='):
        if typ == 'any' or typ == 'all':
            result = 'name' + arg + ''
        else:
            result = '(type=' + typ + ') and (name' + arg + ')'
    elif arg in ['prune', 'flatten']:
        result = arg + ' ' + typ
    elif arg.startswith ('sort'):
        if arg == 'sort':
            result = arg + ' ' + typ + ' text'
        else:
            bits = arg.split ()
            assert len (bits) == 2, 'sort can have one field type argument'
            result = 'sort' + ' ' + typ + ' ' + bits[1]
    else:
        if typ == 'any' or typ == 'all':
            result = arg
        else:
            result = '(type=' + typ + ') and (' + arg + ')'
    logger.debug ("adapted argument: '%s'", result)
    return result

def set_debug_opt (name, value):
    if name== 'now' : 
        the_time = datetime.strptime (value, "%Y-%m-%d")
        cmd_parser.the_time = the_time

if __name__ == "__main__":
    
    today = date.today ()
    time_fmt='%Y-%m-%d'
    opn=False
    project_mode=True
    file_name = None
    infile = None
    template = None
    template_dir = os.environ['OFEXPORT_HOME'] + '/templates/'
    include = True
    
    opts, args = getopt.optlist, args = getopt.getopt(sys.argv[1:],SHORT_OPTS, LONG_OPTS)
    
    assert len (args) == 0, "unexpected arguments: " + str (args)
        
    for opt, arg in opts:
        if '--open' == opt:
            opn = True
        elif '-o' == opt:
            file_name = arg
        elif '-i' == opt:
            infile = arg
        elif '-T' == opt:
            template = load_template (template_dir, arg)
        elif '-v' == opt:
            for logname in LOGGER_NAMES:
                logging.getLogger(logname).setLevel (logging.INFO)
        elif '-V' == opt:
            level = arg
            for logname in LOGGER_NAMES:
                logging.getLogger(logname).setLevel (logging.__dict__[arg])
        elif '-z' == opt:
            for logname in LOGGER_NAMES:
                logging.getLogger(logname).setLevel (logging.DEBUG)
        elif '--log' == opt:
            bits = arg.split('=')
            assert len(bits) == 2
            name = bits[0]
            level = bits[1]
            if name=='ofexport':
                name = __name__
            logging.getLogger(name).setLevel (logging.__dict__[level])
        elif '--debug' == opt:
            bits = arg.split('=')
            assert len(bits) == 2
            name = bits[0]
            value = bits[1]
            set_debug_opt (name, value)
        elif opt in ('-?', '-h', '--help'):
            print_help ()
            sys.exit()
    
    if file_name == None:
            print_help ()
            sys.exit()
    
    if file_name.find ('.') == -1:
        logger.error ('output file name must have suffix: %s', file_name)
        sys.exit()
    dot = file_name.index ('.')
    fmt = file_name[dot+1:]
    
    if infile != None:
        root_project, root_context = read_json (infile)
    else:    
        root_project, root_context = build_model (find_database ())
    
    subject = root_project
        
    for opt, arg in opts:
        logger.debug ("executing option %s : %s", opt, arg)
        visitor = None
        if opt in ('--project', '-p'):
            fixed_arg = fix_abbrieviated_expr(PROJECT, arg)
            visitor = make_filter (fixed_arg, include)
        elif opt in ('--task', '-t'):
            fixed_arg = fix_abbrieviated_expr(TASK, arg)
            visitor = make_filter (fixed_arg, include)
        elif opt in ('--context', '-c'):
            fixed_arg = fix_abbrieviated_expr(CONTEXT, arg)
            visitor = make_filter (fixed_arg, include)
        elif opt in ('--folder', '-f'):
            fixed_arg = fix_abbrieviated_expr(FOLDER, arg)
            visitor = make_filter (fixed_arg, include)
        elif opt in ('--any', '-a'):
            visitor = make_filter (fix_abbrieviated_expr('any', arg), include)
        elif '-C' == opt:
            logger.info ('context mode')
            subject = root_context
        elif '-P' == opt:
            logger.info ('project mode')
            subject = root_project
        elif '-I' == opt:
            logger.info ('include mode')
            include = True
        elif '-E' == opt:
            include = False
            logger.info ('exclude mode')
        
        logger.debug ("created filter %s", visitor)
        if visitor != None:
            logger.info ('running filter %s', visitor)
            traverse (visitor, subject, project_mode=project_mode)
            
    logger.info ('Generating: %s', file_name)
    
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
