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

def load_resource (template_dir, name):
    instream=codecs.open(template_dir + name, 'r', 'utf-8')
    resource = instream.read()
    instream.close ()
    return resource

class FmtTemplate:
    def __init__(self, data):
        self.preamble = None
        self.postamble = None
        self.indent_start = data['indent']
        self.depth_start = data['depth']
        self.indent = data['indentString']
        self.nodes = {k:Template(v) for (k,v) in data['Nodes'].items()}
        self.node_attributes = {k:Template(v) for (k,v) in data['NodeAttributes'].items()}
        self.node_attribute_defaults = data['NodeAttributeDefaults']
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
    def __init__ (self, out, template, attrib_conversions=None):
        if attrib_conversions == None:
            attrib_conversions = {
                      'id'             : lambda x: x,
                      'name'           : lambda x: x,
                      'link'           : lambda x: x,
                      'flagged'        : lambda x: str(x) if x else None,
                      'context'        : lambda x: x.name,
                      'project'        : lambda x: x.name,
                      'date_to_start'  : lambda x: x.strftime(template.date_format),
                      'date_due'       : lambda x: x.strftime(template.date_format),
                      'date_completed' : lambda x: x.strftime(template.date_format),
                      'note'           : lambda x: ''.join([line+'\n' for line in x.get_note_lines ()])
                      }
        
        self.template = template
        self.depth = self.template.indent_start
        self.traversal_depth = self.template.depth_start
        self.out = out
        self.attrib_conversions = attrib_conversions
        self.extra_attribs = {}
    def begin_folder (self, folder):
        self.update_extra_attribs(folder, 'folder')
        line = format_item (folder, self.template, 'FolderStart', self.attrib_conversions, self.extra_attribs)
        if line != None:
            print >>self.out, line
        self.depth+=1
        self.traversal_depth+=1
    def end_folder (self, folder):
        self.depth-=1
        self.traversal_depth-=1
        self.update_extra_attribs(folder, 'folder')
        line = format_item (folder, self.template, 'FolderEnd', self.attrib_conversions, self.extra_attribs)
        if line != None:
            print >>self.out, line
    def begin_project (self, project):
        self.update_extra_attribs(project, 'task')
        line = format_item (project, self.template, 'ProjectStart', self.attrib_conversions, self.extra_attribs)
        if line != None:
            print >>self.out, line
            self.handle_note (project)
        self.depth+=1
        self.traversal_depth+=1
    def end_project (self, project):
        self.depth-=1
        self.traversal_depth-=1
        self.update_extra_attribs(project, 'task')
        line = format_item (project, self.template, 'ProjectEnd', self.attrib_conversions, self.extra_attribs)
        if line != None:
            print >>self.out, line
    def begin_task (self, task):
        self.update_extra_attribs(task, 'task')
        if self.is_empty (task) or self.project_mode == False:
            line = format_item (task, self.template, 'TaskStart', self.attrib_conversions, self.extra_attribs)
            if line != None:
                print >>self.out, line
                self.handle_note (task)
        else:
            line = format_item (task, self.template, 'TaskGroupStart', self.attrib_conversions, self.extra_attribs)
            if line != None:
                print >>self.out, line
                self.handle_note (task)
        self.depth+=1
        self.traversal_depth+=1
    def end_task (self, task):
        self.depth-=1
        self.traversal_depth-=1
        self.update_extra_attribs(task, 'task')
        if self.is_empty (task) or self.project_mode == False:
            line = format_item (task, self.template, 'TaskEnd', self.attrib_conversions, self.extra_attribs)
            if line != None:
                print >>self.out, line
        else:
            line = format_item (task, self.template, 'TaskGroupEnd', self.attrib_conversions, self.extra_attribs)
            if line != None:
                print >>self.out, line
    def begin_context (self, context):
        self.update_extra_attribs(context, 'context')
        line = format_item (context, self.template, 'ContextStart', self.attrib_conversions, self.extra_attribs)
        if line != None:
            print >>self.out, line
        self.depth+=1
        self.traversal_depth+=1
    def end_context (self, context):
        self.depth-=1
        self.traversal_depth-=1
        self.update_extra_attribs(context, 'context')
        line = format_item (context, self.template, 'ContextEnd', self.attrib_conversions, self.extra_attribs)
        if line != None:
            print >>self.out, line
    def is_empty (self, item):
        return len ([x for x in item.children if x.marked]) == 0
    def update_extra_attribs (self, item, link_type):
        self.extra_attribs['depth'] = str (self.traversal_depth)
        self.extra_attribs['indent'] = self.template.indent * (self.depth)
    def handle_note (self, item):
        if item.note != None and 'NoteLine' in self.template.nodes:
            for line in item.note.get_note_lines ():
                self.extra_attribs['note_line'] = line
                print >>self.out, format_item (item, self.template, 'NoteLine', self.attrib_conversions, self.extra_attribs)
        
def build_attrib_values (item, attrib_conversions):
    attrib_values = {}
    for name in item.__dict__.keys():
        if name in attrib_conversions:
            convert = attrib_conversions[name]
            value = item.__dict__[name]
            if value != None:
                str_value = convert (item.__dict__[name])
                if str_value != None:
                    attrib_values[name] = str_value
    return attrib_values

def build_template_substitutions (item, attrib_conversions, attrib_defaults, attrib_templates):
    substitutions = dict (attrib_defaults)
    attrib_values = build_attrib_values (item, attrib_conversions)
    for tpl_key in attrib_templates.keys ():
        if tpl_key in attrib_values:
            attrib_template = attrib_templates[tpl_key]
            value = attrib_values[tpl_key]
            if value != None:
                substitutions[tpl_key] = attrib_template.safe_substitute (value=value)
    return substitutions

def build_entry (item, line_template, attrib_conversions, attrib_defaults, attrib_templates, extra_attribs = {}):
    item_attribs = build_template_substitutions (item, attrib_conversions, attrib_defaults, attrib_templates)
    item_attribs.update (extra_attribs)
    return line_template.safe_substitute(item_attribs)

def format_item (item, template, node_type, attrib_conversions, extra_attribs = {}):
    if node_type in template.nodes:
        return build_entry (item, template.nodes[node_type], attrib_conversions, template.node_attribute_defaults, template.node_attributes, extra_attribs)
    return None

def format_document (root, formatter, project_mode):
    if formatter.template.preamble != None:
        print >>formatter.out, formatter.template.preamble
    traverse_list (formatter, root.children, project_mode=project_mode)
    if formatter.template.postamble != None:
        print >>formatter.out, formatter.template.postamble
