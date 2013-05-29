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

from fmt_template import Formatter, format_document
from ofexport import load_template

def escape (val):
    return val.replace('"','&quot;').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def generate (out, root_project, root_context, project_mode, template_dir, type_config):
    subject = root_project if project_mode else root_context
    template = load_template (template_dir, type_config['template'])
    
    template.attrib_map_builder.type_fns['opml.string'] = lambda x:  escape (x)
    template.attrib_map_builder.type_fns['opml.note'] = lambda x: '&#10;'.join([escape (line) for line in x.get_note_lines ()])
    
    visitor = Formatter (out, template)
    format_document (subject, visitor, project_mode)