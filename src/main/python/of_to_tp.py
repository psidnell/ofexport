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

from fmt_template import Formatter
from string import replace

def remove_trailing_colon (x):
    if x.endswith(':'):
        return x[:-1]
    return x
    
def strip_brackets (x):
    return replace(replace(x, ')', ''), '(','')
    
ATTRIB_CONVERSIONS = {
                      'name'           : lambda x: remove_trailing_colon(x),
                      'link'           : lambda x: x,
                      'flagged'        : lambda x: str(x) if x else None,
                      'context'        : lambda x: strip_brackets(''.join (x.name.split ())),
                      'project'        : lambda x: strip_brackets(''.join (x.name.split ())),
                      'date_to_start'  : lambda x: x.strftime('%Y-%m-%d'),
                      'date_due'       : lambda x: x.strftime('%Y-%m-%d'),
                      'date_completed' : lambda x: x.strftime('%Y-%m-%d')
                      }
    
class PrintTaskpaperVisitor(Formatter):
    def __init__ (self, out, template):
        Formatter.__init__(self, out, template, attrib_conversions=ATTRIB_CONVERSIONS)