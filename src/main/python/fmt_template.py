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

from string import Template

DEFAULT_TEMPLATE = {
                        'indentStart'           : 0,
                        'indent'                : '\t',
                        'Nodes': {
                              'Project'         : 'P $name:$tags',
                              'Folder'          : 'F $name:',
                              'Context'         : 'C $name:',
                              'Task'            : 'T $name $tags',
                              'TaskGroup'       : 'T $name:$tags',
                              },
                        'NodeAttributes'        : {
                              'name'            : '$value',
                              'flagged'         : ' @flagged',
                              'date_to_start'   : ' @start($value)',
                              'date_due'        : ' @due($value)',
                              'date_completed'  : ' @done($value)',
                              'context'         : ' @context($value)',
                              'project'         : ' @project($value)'
                            },
                        'NodeAttributeDefaults' : {
                              'name'            : '',
                              'flagged'         : '',
                              'context'         : '',
                              'project'         : '',
                              'date_to_start'   : '',
                              'date_due'        : '',
                              'date_completed'  : ''
                              }
                    }

class FmtTemplate:
    def __init__(self, data = DEFAULT_TEMPLATE):
        self.indent_start = data['indentStart']
        self.indent = data['indent']
        self.nodes = {k:Template(v) for (k,v) in data['Nodes'].items()}
        self.node_attributes = {k:Template(v) for (k,v) in data['NodeAttributes'].items()}
        self.node_attribute_defaults = data['NodeAttributeDefaults']
        
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
    return build_entry (item, template.nodes[node_type], attrib_conversions, template.node_attribute_defaults, template.node_attributes, extra_attribs)
