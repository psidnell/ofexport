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

from treemodel import Visitor, TASK, PROJECT, CONTEXT, FOLDER
from datematch import process_date_specifier, date_range_to_str
import re
from datetime import datetime

INCLUDED='INCLUDED'
EXCLUDED='EXCLUDED'
PATH_TO_INCLUDED='PATH_TO_INCLUDED'

def get_name (item):
    return item.name

def get_start (item):
    if not 'start' in item.__dict__ or  item.start == None:
        return datetime.now()
    return item.start

def get_due (item):
    if not 'due' in item.__dict__ or item.due == None:
        return datetime.now()
    return item.due

def get_flagged (item):
    return item.flagged

def get_completion (item):
    if not 'date_completed' in item.__dict__ or item.date_completed == None:
        return datetime.now()
    return item.date_completed

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

def set_attrib_to_root (path_to_root, name, value):
    for item in path_to_root:
        item.attribs[name] = value

def mark_branch_not_marked (item, project_mode):
    if item.marked:
        item.marked = False
        if (item.type == TASK or item.type == PROJECT) and not project_mode:
            # We only got here because we recursed from a context
            # Tasks/Projects are not a tree in context mode, they're flat so we don't want
            # to un-mark all the children since they might be in a different context
            return
        for child in item.children:
            mark_branch_not_marked (child, project_mode)
            
class BaseFilterVisitor(Visitor):
    def __init__(self, include=True):
        self.filter = None
        self.include = include
        self.traversal_path = []
    def begin_any (self, item):
        # Can't use the item parent since this only has meaning
        # in project mode - have to track our own traversal path
        parent = None
        if len(self.traversal_path) > 0:
            parent = self.traversal_path[-1]
        item.attribs[PATH_TO_INCLUDED] = False
        if parent != None:
            # Inherit these attribute
            item.attribs[INCLUDED] = parent.attribs[INCLUDED]
            item.attribs[EXCLUDED] = parent.attribs[EXCLUDED]
            assert parent.attribs[INCLUDED] != None, "missing attribute in " + parent.name
            assert parent.attribs[EXCLUDED] != None, "missing attribute in " + parent.name
        else:
            item.attribs[INCLUDED] = False
            item.attribs[EXCLUDED] = False
        self.traversal_path.append(item)
    def end_any (self, item):
        assert item.attribs[PATH_TO_INCLUDED] != None, "missing attribute in " + item.name
        assert item.attribs[INCLUDED] != None, "missing attribute in " + item.name
        assert item.attribs[EXCLUDED] != None, "missing attribute in " + item.name
        self.traversal_path.pop()
        if self.include and not (item.attribs[INCLUDED] or item.attribs[PATH_TO_INCLUDED]):
            mark_branch_not_marked (item, self.project_mode)
        # We've finished processing the node, tidy up
        # and avoid confusing the next filter.
        del (item.attribs[INCLUDED])
        del (item.attribs[EXCLUDED])
        del (item.attribs[PATH_TO_INCLUDED])
    def match_required (self, item):
        if item.attribs[INCLUDED] or item.attribs[EXCLUDED]:
            # The decision has already been made
            return False
        return True
    def set_item_matched (self, item, matched):
        # invoked from begin_XXX
        if self.include:
            if matched:
                # Then we want this node in the output and want to stop
                # this filter testing removing any parents or children of this node
                item.attribs[INCLUDED] = True
                set_attrib_to_root (self.traversal_path, PATH_TO_INCLUDED, True)
        else: # In exclude mode
            if matched:
                # This node is toast
                mark_branch_not_marked (item, self.project_mode)
            else:
                # We haven't excluded it so it stays
                pass

def includes (include):
    if include:
        return 'include'
    else:
        return 'exclude'
    
class Filter(BaseFilterVisitor):
    def __init__(self, types, match_fn, filtr, include, nice_string):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
        self.types = types
        self.match_fn = match_fn
        self.nice_string = nice_string
    def begin_any (self, item):
        BaseFilterVisitor.begin_any (self, item)
        if item.type in self.types and self.match_required(item):
            matched = self.match_fn(item, self.filter)
            self.set_item_matched(item, matched);
    def __str__(self):
        return includes (self.include) + ' ' + str(self.types) + ' where ' + self.nice_string
    
class Sort(Visitor):
    def __init__(self, types, get_key_fn, nice_string):
        Visitor.__init__(self)
        self.types = types
        self.get_key_fn = get_key_fn
        self.nice_string = nice_string
    def begin_any (self, item):
        if item.type in self.types:
            self.sort_list(item.children)
    def sort_list (self, items):
        items.sort(key=lambda x:self.get_key_fn (x))
    def __str__(self):
        return 'sort ' + str(self.types) + ' by ' + self.nice_string

class Prune (Visitor):
    def __init__(self, types):
        Visitor.__init__(self)
        self.types = types
    def end_any (self, item):
        if item.type in self.types:
            self.prune_if_empty(item)
    def prune_if_empty (self, item):
        if item.marked:
            empty = len ([x for x in item.children if x.marked]) == 0
            if empty:
                item.marked = False
    def __str__ (self):
        return 'prune ' + str(self.types)


    
class Flatten (Visitor):
    def __init__(self, types):
        Visitor.__init__(self)
        self.types = types
    def end_any (self, item):
        self.flatten (item)
    def flatten (self, item):
        new_children = []
        for child in item.children:
            if child.type in self.types:
                for grandchild in list(child.children):
                    if grandchild.type == child.type or child.type == FOLDER:
                        new_children.append(grandchild)
                        child.children.remove (grandchild)
            new_children.append(child)
        item.children = []
        for child in new_children:
            item.add_child (child)
    def __str__ (self):
        return 'Flatten'
     
#-----------------------------------

class NameFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
        self.match_fn = match_name
    def begin_any (self, item):
        BaseFilterVisitor.begin_any (self, item)
        if self.match_required(item):
            matched = self.match_fn(item, self.filter)
            self.set_item_matched(item, matched);
    def __str__(self):
        return 'name ' + includes (self.include) + ' "' + self.filter + '"'
    
class FlaggedFilterVisitor(BaseFilterVisitor):
    def __init__(self, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.match_fn = match_flagged
    def begin_any (self, item):
        BaseFilterVisitor.begin_any (self, item)
        if self.match_required(item):
            if item.type == PROJECT or item.type == TASK:
                matched = self.match_fn(item, self.filter)
                self.set_item_matched(item, matched);
    def __str__(self):
        return 'name ' + includes (self.include) + ' flagged'

class FolderFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, match_fn, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
        self.match_fn = match_fn
    def begin_folder (self, folder):
        if self.match_required(folder):
            matched = self.match_fn(folder, self.filter)
            self.set_item_matched(folder, matched);
            
class TaskFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, match_fn, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
        self.match_fn = match_fn
    def begin_task (self, task):
        if self.match_required(task):
            matched = self.match_fn(task, self.filter)
            self.set_item_matched(task, matched);
            
class ProjectFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, match_fn, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
        self.match_fn = match_fn
    def begin_project (self, project):
        if self.match_required(project):
            matched = self.match_fn(project, self.filter)
            self.set_item_matched(project, matched);
                    
class ProjectAndTaskFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, match_fn, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
        self.match_fn = match_fn
    def begin_task (self, task):
        if self.match_required(task):
            matched = self.match_fn(task, self.filter)
            self.set_item_matched(task, matched);
    def begin_project (self, project):
        if self.match_required(project):
            matched = self.match_fn(project, self.filter)
            self.set_item_matched(project, matched);
            
class ContextFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, match_fn, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
        self.match_fn = match_fn
    def begin_context (self, context):
        if self.match_required(context):
            matched = self.match_fn(context, self.filter)
            self.set_item_matched(context, matched);

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
    
class StartFilterVisitor(ProjectAndTaskFilterVisitor):
    def __init__(self, filtr, include=True):
        ProjectAndTaskFilterVisitor.__init__(self, process_date_specifier (datetime.now(), filtr), match_start, include)
    def __str__(self):
        return 'Start ' + includes (self.include) + ' ' + date_range_to_str(self.filter)
    
class DueFilterVisitor(ProjectAndTaskFilterVisitor):
    def __init__(self, filtr, include=True):
        ProjectAndTaskFilterVisitor.__init__(self, process_date_specifier (datetime.now(), filtr), match_due, include)
    def __str__(self):
        return 'Due ' + includes (self.include) + ' ' + date_range_to_str(self.filter)
    
class CompletionFilterVisitor(ProjectAndTaskFilterVisitor):
    def __init__(self, filtr, include=True):
        ProjectAndTaskFilterVisitor.__init__(self, process_date_specifier (datetime.now(), filtr), match_completed, include)
    def __str__(self):
        return 'Completion ' + includes (self.include) + ' ' + date_range_to_str(self.filter)
        
class TaskFlaggedFilterVisitor(TaskFilterVisitor):
    def __init__(self, include=True):
        TaskFilterVisitor.__init__(self, None, match_flagged, include)
    def __str__(self):
        return 'Task flagged ' + includes (self.include) + ' flagged'

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

class ContextNameSortingVisitor (Visitor):
    def end_context (self, folder):
        folder.children.sort(key=lambda item:item.name)
    def __str__ (self):
        return 'Folders/Projects sorted by name'
    
class NameSortingVisitor (Visitor):
    def end_any (self, item):
        item.children.sort(key=lambda x:x.name)
    def __str__ (self):
        return 'Sort by name'

def flatten (item):
    new_children = []
    for child in item.children:
        # Add this nodes children above itself,
        # this is the omnifocus way.
        flatten (child)
        new_children = new_children + child.children
        new_children.append(child)
        child.children = []
    item.children = new_children

class FlatteningVisitor (Visitor):
    def __init__(self):
        self.projects = []
        self.contexts = []
    def end_project (self, project):
        self.projects.append(project)
        flatten (project)
        for child in project.children:
            child.parent = project        
    def end_task (self, task):
        flatten (task)
        for child in task.children:
            child.parent = task
    def end_context (self, context):
        new_children = []
        for child in context.children:
            if child.type != CONTEXT:
                new_children.append (child)
                child.parent = None
        context.children = new_children
        self.contexts.append(context)   
    def __str__ (self):
        return 'Flatten'

class PruningFilterVisitor (Visitor):
    def end_project (self, project):
        if self.project_mode:
            self.prune_if_empty(project)
        else:
            project.match = False
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
