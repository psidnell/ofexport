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

from string import replace
from ofexport import load_template
from fmt_template import Formatter, format_document

def remove_trailing_colon (x):
    if x.endswith(':'):
        return x[:-1]
    return x
    
def strip_brackets (x):
    return replace(replace(x, ')', ''), '(','')

def generate (out, root_project, root_context, project_mode, template_dir, type_config):
    subject = root_project if project_mode else root_context
    template = load_template (template_dir, type_config['template'])
    
    template.attrib_map_builder.type_fns['taskpaper.tag'] = lambda x:  strip_brackets(''.join (x.split ()))
    template.attrib_map_builder.type_fns['taskpaper.title'] = lambda x: remove_trailing_colon(x)
    
    visitor = Formatter (out, template)
    format_document (subject, visitor, project_mode)