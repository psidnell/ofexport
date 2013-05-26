from fmt_template import Formatter
from ofexport import load_template, format_document

def escape (val):
    return val.replace('"','&quot;').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def generate (out, root_project, root_context, project_mode, template_dir, type_config):
    subject = root_project if project_mode else root_context
    template = load_template (template_dir, type_config['template'])
    
    template.attrib_map_builder.type_fns['html.string'] = lambda x:  escape (x)
    template.attrib_map_builder.type_fns['html.note'] = lambda x: ''.join([line+'<br>' for line in x.get_note_lines ()])

    visitor = Formatter (out, template)
    format_document (subject, visitor, project_mode)