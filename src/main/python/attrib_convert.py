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

class Conversion:
    def __init__ (self, field, default, format_template, typ, evaluate = None):
        self.field = field
        self.evaluate = evaluate
        self.type = typ
        self.format_template = Template(format_template)
        self.default = default            
    def value (self, node, type_fns):
        # Does the attrib have the attribute at all?
        # If not use the template default 
        if not self.field in node.__dict__:
            return self.default
        
        value = node.__dict__[self.field]
        
        # If it's null use the demplate default
        if value == None:
            return self.default
        
        # Run optional custom code, for example loading
        # a sub attribute of the object
        if self.evaluate != None:
            value = eval (self.evaluate) 
        
        # If that yielded null use the template default
        if value == None:
            return self.default
        
        # Run a converter assocuated with it's type
        # Possibly loaded from a plugin
        value = type_fns[self.type] (value) 
        
        # If that yielded null use the template default
        if value == None:
            return self.default
        
        # Finally, having got a non-null string format it with the format associated with the field
        return self.format_template.safe_substitute (value=value)
        
class AttribMapBuilder:
    def __init__ (self):
        
        self.type_fns = {}
        self.type_fns['string'] = lambda x: x
        self.type_fns['date'] = lambda x: x.strftime(self.date_format)
        self.type_fns['boolean'] = lambda x: str (x)
        self.type_fns['note'] = lambda x: x.get_note ()
        
        self.attrib_conversions = {}
        self.set_conversion(Conversion("id", "", "$value", "string"))
        self.set_conversion(Conversion("type", "", "$value", "string"))
        self.set_conversion(Conversion("name", "", "$value", "string"))
        self.set_conversion(Conversion("link", "", "$value", "string"))
        self.set_conversion(Conversion("status", "", "$value", "string"))
        self.set_conversion(Conversion("flagged", "", "$value", "boolean"))
        self.set_conversion(Conversion("context", "", "$value", "string", "value.name"))
        self.set_conversion(Conversion("project", "", "$value", "string", "value.name"))
        self.set_conversion(Conversion("date_to_start", "", "$value", "date"))
        self.set_conversion(Conversion("date_due", "", "$value", "date"))
        self.set_conversion(Conversion("date_complete", "", "$value", "date"))
        self.set_conversion(Conversion("note", "", "$value", "note"))
        
        self.date_format = "%Y-%m-%d"
    def set_conversion (self, attrib):
        self.attrib_conversions[attrib.field] = attrib
    def get_values (self, x):
        result = {}
        for conversion in self.attrib_conversions.values():
            key = conversion.field
            value = conversion.value (x, self.type_fns)
            result[key] = value
        return result
    