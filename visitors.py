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

from treemodel import Visitor
from datematch import process_date_specifier
import re
from datetime import datetime

SELECTED='visitors.selected'

def match_name (item, regexp):
        return re.search (regexp, item.name) != None

def match_date_against_range (thedate, date_range):
    start, end = date_range
    if start == None and end == None:
        return thedate == None
    elif thedate == None:
        return start == None and end == None
    elif start != None and end != None:
        return thedate.date() >= start.date() and thedate.date() <= end.date ()
    elif start != None:
        return thedate.date() >= start.date()
    else:
        return thedate.date() <= end.date ()
        
def match_start (item, date_range):
    return match_date_against_range (item.date_to_start, date_range)

def match_due (item, date_range):
    return match_date_against_range (item.date_due, date_range)

def match_completed (item, date_range):
    return match_date_against_range (item.date_completed, date_range)

def match_flagged (item, ignore):
        return item.flagged

'''
When we explicitly match an item we want all it's descendants
matched unconditionally - even if they would have failed the match
we're running. The marked flag isn't enough since it's set by default
so we need another to represent the selection status just while we're
running a particular filter. We must remember to remove it when we're
done with a node or subsequent filters won't work properly
'''
class BaseFilterVisitor(Visitor):
    def __init__(self, include=True):
        self.filter = None
        self.include = include
    def begin_any (self, item):
        # inherit the SELECTED status
        if item.parent == None:
            item.attribs[SELECTED] = False
        else:
            item.attribs[SELECTED] = item.parent.attribs[SELECTED]
    def end_any (self, item):
        del item.attribs[SELECTED] # for the next filter
    def set_item_matched (self, item, matched):
        if not self.include:
            matched = not matched
        item.marked = matched
        item.attribs[SELECTED] = True

class FolderFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, match_fn, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
        self.match_fn = match_fn
    def begin_folder (self, folder):
        if not folder.attribs[SELECTED]:
            matched = self.match_fn(folder, self.filter)
            self.set_item_matched(folder, matched);
            
class TaskFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, match_fn, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
        self.match_fn = match_fn
    def begin_task (self, task):
        if not task.attribs[SELECTED]:
            matched = self.match_fn(task, self.filter)
            self.set_item_matched(task, matched);
            
class ProjectFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, match_fn, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
        self.match_fn = match_fn
    def begin_project (self, project):
        if not project.attribs[SELECTED]:
            matched = self.match_fn(project, self.filter)
            self.set_item_matched(project, matched);
            
class ContextFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, match_fn, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
        self.match_fn = match_fn
    def begin_context (self, context):
        if not context.attribs[SELECTED]:
            matched = self.match_fn(context, self.filter)
            self.set_item_matched(context, matched);

def includes (include):
    if include:
        return 'includes'
    else:
        return 'excludes'
    
def date_range_to_str (spec):
    fmt = "[%a %b %d %Y]"
    start, end = spec
    if start == None and end == None:
        return 'none'
    elif start == None and end != None:
        return 'everything until ' + end.strftime (fmt)
    elif start != None and end == None:
        return 'everything after ' + start.strftime (fmt)
    elif start == end:
        return 'on ' + start.strftime (fmt)
    else:
        return 'from ' + start.strftime (fmt) + ' to ' + end.strftime (fmt)
    

class FolderNameFilterVisitor(FolderFilterVisitor):
    def __init__(self, filtr, include=True):
        FolderFilterVisitor.__init__(self, filtr, match_name, include)
    def __str__(self):
        return 'Folder name ' + includes (self.include) + ' "' + self.filter + '"'

class ProjectNameFilterVisitor(ProjectFilterVisitor):
    def __init__(self, filtr, include=True):
        ProjectFilterVisitor.__init__(self, filtr, match_name, include)
    def __str__(self):
        return 'Project name ' + includes (self.include) + ' "' + self.filter + '"'

class ContextNameFilterVisitor(ContextFilterVisitor):
    def __init__(self, filtr, include=True):
        ContextFilterVisitor.__init__(self, filtr, match_name, include)
    def __str__(self):
        return 'Context name ' + includes (self.include) + ' "' + self.filter + '"'
            
class TaskNameFilterVisitor(TaskFilterVisitor):
    def __init__(self, filtr, include=True):
        TaskFilterVisitor.__init__(self, filtr, match_name, include)
    def __str__(self):
        return 'Task name ' + includes (self.include) + ' "' + self.filter + '"'
            
class ProjectCompletionFilterVisitor(ProjectFilterVisitor):
    def __init__(self, filtr, include=True):
        ProjectFilterVisitor.__init__(self, process_date_specifier (datetime.now(), filtr), match_completed, include)
    def __str__(self):
        return 'Project completion ' + includes (self.include) + ' ' + date_range_to_str(self.filter)
        
class ProjectStartFilterVisitor(ProjectFilterVisitor):
    def __init__(self, filtr, include=True):
        ProjectFilterVisitor.__init__(self, process_date_specifier (datetime.now(), filtr), match_start, include)
    def __str__(self):
        return 'Project start ' + includes (self.include) + ' ' + date_range_to_str(self.filter)
        
class ProjectDueFilterVisitor(ProjectFilterVisitor):
    def __init__(self, filtr, include=True):
        ProjectFilterVisitor.__init__(self, process_date_specifier (datetime.now(), filtr), match_due, include)
    def __str__(self):
        return 'Project due ' + includes (self.include) + ' ' + date_range_to_str(self.filter)
        
class ProjectFlaggedFilterVisitor(ProjectFilterVisitor):
    def __init__(self, include=True):
        ProjectFilterVisitor.__init__(self, None, match_flagged, include)
    def __str__(self):
        return 'Project flagged ' + includes (self.include) + ' flagged'

class TaskCompletionFilterVisitor(TaskFilterVisitor):
    def __init__(self, filtr, include=True):
        TaskFilterVisitor.__init__(self, process_date_specifier (datetime.now(), filtr), match_completed, include)
    def __str__(self):
        return 'Task completion ' + includes (self.include) + ' ' + date_range_to_str(self.filter)

class TaskDueFilterVisitor(TaskFilterVisitor):
    def __init__(self, filtr, include=True):
        TaskFilterVisitor.__init__(self, process_date_specifier (datetime.now(), filtr), match_due, include)
    def __str__(self):
        return 'Task due ' + includes (self.include) + ' ' + date_range_to_str(self.filter)
        
class TaskStartFilterVisitor(TaskFilterVisitor):
    def __init__(self, filtr, include=True):
        TaskFilterVisitor.__init__(self, process_date_specifier (datetime.now(), filtr), match_start, include)
    def __str__(self):
        return 'Task start ' + includes (self.include) + ' ' + date_range_to_str(self.filter)
        
class TaskFlaggedFilterVisitor(TaskFilterVisitor):
    def __init__(self, include=True):
        TaskFilterVisitor.__init__(self, None, match_flagged, include)
    def __str__(self):
        return 'Task flagged ' + includes (self.include) + ' flagged'

class FlatteningVisitor (Visitor):
    def __init__(self):
        self.projects = []
    def begin_project (self, project):
        self.projects.append(project)
    def end_task (self, task):
        mypos = task.parent.children.index (task)
        # Add this nodes children above itself,
        # this is the omnifocus way.
        for child in task.children:
            task.parent.children.insert (mypos, child)
            child.parent = task.parent
        task.children = []
    def __str__ (self):
        return 'Flatten'
        
class TaskCompletionSortingVisitor (Visitor):
    def end_project (self, project):
        project.children.sort(key=lambda item:self.get_key(item))
    def get_key (self, item):
        if item.date_completed != None:
            return item.date_completed
        return datetime.today()
    def __str__ (self):
        return 'Tasks sorted by completion'
    
class FolderNameSortingVisitor (Visitor):
    def end_folder (self, folder):
        folder.children.sort(key=lambda item:item.name)
    def __str__ (self):
        return 'Folders/Projects sorted by name'
    
class PruningFilterVisitor (Visitor):
    def end_project (self, project):
        self.prune_if_empty(project)
    def end_folder (self, folder):
        self.prune_if_empty(folder)
    def end_context (self, context):
        self.prune_if_empty(context)
    def prune_if_empty (self, item):
        if item.marked:
            empty = len ([x for x in item.children if x.marked]) == 0
            if empty:
                item.marked = False
    def __str__ (self):
        return 'Prune'     
