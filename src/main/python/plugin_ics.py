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

from datetime import datetime, timedelta
from fmt_template import Formatter, format_document
import time
import logging
from ofexport import load_template


logger = logging.getLogger(__name__)

DATE_FORMAT_LONG = "%Y%m%dT%H%M00Z"
DATE_FORMAT_SHORT = "%Y%m%d"

def generate (out, root_project, root_context, project_mode, template_dir, type_config):
    subject = root_project if project_mode else root_context
    template = load_template (template_dir, type_config['template'])
    time_control_default = type_config["time_control_default"]
    logger.debug ("time_control_default: %s", time_control_default)
    visitor = PrintCalendarVisitor (out, template, time_control_default)
    format_document (subject, visitor, project_mode)

class PrintCalendarVisitor(Formatter):
    def __init__ (self, out, template, time_control_default):
        Formatter.__init__(self, out, template)
        self.current_item = None
        self.time_control_default = time_control_default

        # Start and due dates are formated differently for all day tasks, need different types
        template.attrib_map_builder.type_fns['ics.date_due'] = lambda x: format_date(self.current_item, x, True)
        template.attrib_map_builder.type_fns['ics.date_to_start'] = lambda x: format_date(self.current_item, x, False)
        template.attrib_map_builder.type_fns['ics.note'] = lambda x: '\\r'.join(x.get_note_lines ())
         
    def begin_any (self, item):
        Formatter.begin_any(self, item)
        self.current_item = item
    def end_any (self, item):
        pass
    def begin_folder (self, folder):
        pass
    def end_folder (self, folder):
        pass
    def begin_project (self, project):
        if project.date_due != None or project.date_to_start != None:
            fix_dates(project)
            load_note_attribs (project, self.time_control_default)
            Formatter.begin_project(self, project)
    def end_project (self, project):
        if project.date_due != None or project.date_to_start != None:
            Formatter.end_project(self, project)
    def begin_task (self, task):
        if task.date_due != None or task.date_to_start != None:
            fix_dates(task)
            load_note_attribs (task, self.time_control_default)
            Formatter.begin_task(self, task)
    def end_task (self, task):
        if task.date_due != None or task.date_to_start != None:
            Formatter.end_task(self, task)
    def begin_context (self, context):
        pass
    def end_context (self, context):
        pass
    def add_extra_template_attribs (self, item, attribs):
        item.attribs['attrib_cache']['alarm'] = format_alarm (item)
    
def fix_dates (item):
    if item.date_to_start == None and item.date_due == None:
        return
    if item.date_to_start == None and item.date_due != None:
        item.date_to_start = item.date_due
    elif item.date_to_start != None and item.date_due == None:
        item.date_due = item.date_to_start

def load_note_attribs (item, time_control_default):
    logger.debug ("loading note attributes %s %s", item.id, item.name)
    found_directive = False
    if item.note != None:
        for line in item.note.get_note_lines ():
            found_directive = process_line_for_directives (item, line, found_directive)
    if not found_directive and len (time_control_default.strip()) > 0:
        found_directive = process_line_for_directives (item, time_control_default, found_directive)
    
    if found_directive:
        logger.debug ("attributes for %s are %s", item.id, item.attribs)
        
        if 'onstart' in item.attribs:
            item.date_due = item.date_to_start
        if 'ondue' in item.attribs:
            item.date_to_start = item.date_due
        try:
            if 'start' in item.attribs:
                bits = item.attribs['start'].split(':')
                the_date = item.date_to_start
                if len(bits) == 2:
                    item.date_to_start = datetime (the_date.year, the_date.month, the_date.day, int(bits[0]), int(bits[1]), 0, 0, the_date.tzinfo)
                else:
                    logger.error ("problem parsing cal directives, start malformed: %s %s", item.id, item.name)
            if 'due' in item.attribs:
                bits = item.attribs['due'].split(':')
                the_date = item.date_due
                if len(bits) == 2:
                    item.date_due = datetime (the_date.year, the_date.month, the_date.day, int(bits[0]), int(bits[1]), 0, 0, the_date.tzinfo)
                else:
                    logger.error ("problem parsing cal directives, due malformed: %s %s", item.id, item.name)
        except Exception as e:
            logger.error (e.message)
            logger.error ("problem parsing cal directives: %s %s", item.id, item.name)
        if item.date_to_start > item.date_due:
            logger.error ("problem parsing cal directives, the start date is after the due date: %s %s", item.id, item.name)
            item.date_to_start = item.date_due
        logger.debug ("final dates for %s are start:%s due:%s", item.id, item.date_to_start, item.date_due)

def process_line_for_directives (item, line, found_directive):
    if line.strip().startswith('%of'):
        bits = line.split()
        if len(bits) >= 3 and bits[1] == 'cal':
            found_directive = True
            logger.debug ("found directive in %s %s", item.id, line)
            for flag in bits[2:]:
                bits2 = flag.split('=')
                if len(bits2) == 2:
                    item.attribs[bits2[0]] = bits2[1]
                else:
                    item.attribs[flag] = True
    return found_directive
    
def format_date (item, the_date, is_due_date):
    if 'allday' in item.attribs:
        # Make all day - must have no hms in format
        #DTSTART;VALUE=DATE:20020923
        #DTEND;VALUE=DATE:20020924
        the_date = datetime (the_date.year, the_date.month, the_date.day, 0, 0, 0)
        if is_due_date:
            the_date = the_date + timedelta (days=1)
        # NO UTC CONVERSION - it happens on the day we asked for - no adjustment required
        result = the_date.strftime(DATE_FORMAT_SHORT) 
    else:
        the_date = utc (the_date)   
        result = the_date.strftime(DATE_FORMAT_LONG)
    typ = 'due' if is_due_date else 'start'
    logger.debug ("formatted date for %s is %s:%s", item.id, typ, result)
    return result

def utc (the_date):
    epoch_second = time.mktime(the_date.timetuple())
    return datetime.utcfromtimestamp(epoch_second)

def format_alarm (item):
    if "noalarm" in item.attribs:
        return ""
    return "BEGIN:VALARM\nACTION:DISPLAY\nDESCRIPTION:OmniFocus Reminder\nTRIGGER:-PT0M\nEND:VALARM\n"