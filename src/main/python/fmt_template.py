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
from string import Template
from treemodel import Visitor, traverse_list
import codecs
import logging
import sys
from attrib_convert import AttribMapBuilder, Conversion

logging.basicConfig(format='%(asctime)-15s %(name)s %(levelname)s %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.ERROR)

def load_resource (template_dir, name):
    instream=codecs.open(template_dir + name, 'r', 'utf-8')
    resource = instream.read()
    instream.close ()
    return resource

class FmtTemplate:
    def __init__(self, data):
        
        self.attrib_map_builder = AttribMapBuilder ()
        for attrib in data['attributes'].keys():
            attrib_cfg = data['attributes'][attrib]
            evaluate = None
            if 'eval' in attrib_cfg:
                evaluate = attrib_cfg['eval']
            conversion = Conversion (attrib, attrib_cfg['default'], attrib_cfg['format'], attrib_cfg['type'], evaluate=evaluate)
            self.attrib_map_builder.set_conversion(conversion)
        self.attrib_map_builder.date_format = data['dateFormat']
        
        self.preamble = None
        self.postamble = None
        self.indent_start = data['indent']
        self.depth_start = data['depth']
        self.indent = data['indentString']
        self.nodes = {k:Template(v) for (k,v) in data['nodes'].items()}
        self.date_format = data['dateFormat']
        template_dir = os.environ['OFEXPORT_HOME'] + '/templates/'
        if 'preambleFile' in data:
            self.preamble = load_resource (template_dir, data['preambleFile'])
        elif 'preamble' in data:
            self.preamble = data['preamble']
        if 'postambleFile' in data:
            self.postamble = load_resource (template_dir, data['postambleFile'])
        elif 'postamble' in data:
            self.postamble = data['postamble']
        
class Formatter(Visitor):
    def __init__ (self, out, template):
        self.template = template
        self.depth = self.template.indent_start
        self.traversal_depth = self.template.depth_start
        self.out = out
    def begin_folder (self, folder):
        self.update_attribs(folder, 'folder')
        line = format_item (self.template, 'FolderStart', folder.attribs['attrib_cache'])
        if line != None:
            print >>self.out, line
        self.depth+=1
        self.traversal_depth+=1
    def end_folder (self, folder):
        self.depth-=1
        self.traversal_depth-=1
        self.update_attribs(folder, 'folder')
        line = format_item (self.template, 'FolderEnd', folder.attribs['attrib_cache'])
        if line != None:
            print >>self.out, line
    def begin_project (self, project):
        self.update_attribs(project, 'task')
        line = format_item (self.template, 'ProjectStart', project.attribs['attrib_cache'])
        if line != None:
            print >>self.out, line
            self.handle_note (project)
        self.depth+=1
        self.traversal_depth+=1
    def end_project (self, project):
        self.depth-=1
        self.traversal_depth-=1
        self.update_attribs(project, 'task')
        line = format_item (self.template, 'ProjectEnd', project.attribs['attrib_cache'])
        if line != None:
            print >>self.out, line
    def begin_task (self, task):
        self.update_attribs(task, 'task')
        if self.is_empty (task) or self.project_mode == False:
            line = format_item (self.template, 'TaskStart', task.attribs['attrib_cache'])
            if line != None:
                print >>self.out, line
                self.handle_note (task)
        else:
            line = format_item (self.template, 'TaskGroupStart', task.attribs['attrib_cache'])
            if line != None:
                print >>self.out, line
                self.handle_note (task)
        self.depth+=1
        self.traversal_depth+=1
    def end_task (self, task):
        self.depth-=1
        self.traversal_depth-=1
        self.update_attribs(task, 'task')
        if self.is_empty (task) or self.project_mode == False:
            line = format_item (self.template, 'TaskEnd', task.attribs['attrib_cache'])
            if line != None:
                print >>self.out, line
        else:
            line = format_item (self.template, 'TaskGroupEnd', task.attribs['attrib_cache'])
            if line != None:
                print >>self.out, line
    def begin_context (self, context):
        self.update_attribs(context, 'context')
        line = format_item (self.template, 'ContextStart', context.attribs['attrib_cache'])
        if line != None:
            print >>self.out, line
        self.depth+=1
        self.traversal_depth+=1
    def end_context (self, context):
        self.depth-=1
        self.traversal_depth-=1
        self.update_attribs(context, 'context')
        line = format_item (self.template, 'ContextEnd', context.attribs['attrib_cache'])
        if line != None:
            print >>self.out, line
    def end_any (self, item):
        del item.attribs['attrib_cache']
    def is_empty (self, item):
        return len ([x for x in item.children if x.marked]) == 0
    def handle_note (self, item):
        if item.note != None and 'NoteLine' in self.template.nodes:
            for line in item.note.get_note_lines ():
                item.attribs['attrib_cache']['note_line'] = line
                print >>self.out, format_item (self.template, 'NoteLine', item.attribs['attrib_cache'])
    def update_attribs (self, item, link_type):
        if not 'attrib_cache' in item.attribs:
            attribs = self.template.attrib_map_builder.get_values (item)
            item.attribs['attrib_cache'] = attribs
            attribs['depth'] = str (self.traversal_depth)
            attribs['indent'] = self.template.indent * (self.depth)
            self.add_extra_template_attribs(item, attribs)
    def add_extra_template_attribs (self, item, attribs):
        pass

def build_entry (line_template, attributes):
    return line_template.safe_substitute(attributes)

def format_item (template, node_type, attributes):
    if node_type in template.nodes:
        return build_entry (template.nodes[node_type], attributes)
    return None

def format_document (root, formatter, project_mode):
    if formatter.template.preamble != None:
        print >>formatter.out, formatter.template.preamble
    traverse_list (formatter, root.children, project_mode=project_mode)
    if formatter.template.postamble != None:
        print >>formatter.out, formatter.template.postamble
