from fmt_template import Formatter

def escape (val):
    return val.replace('"','&quot;').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    
class PrintOpmlVisitor(Formatter):
    def __init__ (self, out, template):
        attrib_conversions = {
                      'id'             : lambda x: escape(x),
                      'name'           : lambda x: escape(x),
                      'link'           : lambda x: x,
                      'flagged'        : lambda x: str(x) if x else None,
                      'context'        : lambda x: escape(''.join (x.name.split ())),
                      'project'        : lambda x: escape(''.join (x.name.split ())),
                      'date_to_start'  : lambda x: x.strftime(template.date_format),
                      'date_due'       : lambda x: x.strftime(template.date_format),
                      'date_completed' : lambda x: x.strftime(template.date_format)
                      }
        Formatter.__init__(self, out, template, attrib_conversions = attrib_conversions)