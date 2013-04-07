from treemodel import Visitor
import re
from datetime import datetime

class BaseFilterVisitor(Visitor):
    def __init__(self, include=True):
        self.include = include
        self.node_path = []
    def begin_project (self, project):
        self.begin_item(project)
    def end_project (self, project):
        self.end_item (project)
    def begin_folder (self, folder):
        self.begin_item(folder)
    def end_folder (self, folder):
        self.end_item(folder)
    def begin_context (self, context):
        self.begin_item(context)
    def end_context (self, context):
        self.end_item (context)
    def begin_task (self, task):
        self.begin_item (task)
    def end_task (self, task):
        self.end_item (task)
    def begin_item (self, item):
        self.inherit_parent_attribs (item)
        self.node_path.append(item)
    def end_item (self, item):
        self.node_path.remove(item)
    def set_item_matched (self, item, matched):
        if not self.include:
            matched = not matched
        item.attribs['matched_filter'] = True
        if matched:
            # Mark all the way to root
            for node in self.node_path:
                node.marked = True
        else:
            # match failed
            item.marked = False
    def match_name (self, item, regexp):
        return re.search (regexp, item.name) != None
    def match_completed (self, item, regexp):
        if item.date_completed != None:
            # be careful - we want whole days, life gets confusing if we want to see
            # todays tasks but we also see some of yesterdays since it's <24hrs ago 
            days_elapsed = (datetime.today().date() - item.date_completed.date()).days
            date_str = item.date_completed.strftime ('%Y-%m-%d %A %B') + ' -' + str (days_elapsed) +'d'
        else:
            date_str = ''
        return re.search (regexp, date_str) != None
    def inherit_parent_attribs (self, item):
        item.attribs['matched_filter'] = False
        if len(self.node_path) > 0:
            parent = self.node_path[len(self.node_path) - 1]
            item.attribs.update(parent.attribs)

class FolderNameFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
    def begin_folder (self, folder):
        self.begin_item(folder)
        if not folder.attribs['matched_filter'] and self.filter != None:
            matched = self.match_name(folder, self.filter)
            self.set_item_matched(folder, matched);

class ProjectNameFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
    def begin_project (self, project):
        self.begin_item(project)
        if not project.attribs['matched_filter'] and self.filter != None:
            matched = self.match_name(project, self.filter)
            self.set_item_matched(project, matched);

class ContextNameFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
    def begin_context (self, project):
        self.begin_item(project)
        if not project.attribs['matched_filter'] and self.filter != None:
            matched = self.match_name(project, self.filter)
            self.set_item_matched(project, matched);
            
class TaskNameFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
    def begin_task (self, project):
        self.begin_item(project)
        if not project.attribs['matched_filter'] and self.filter != None:
            matched = self.match_name(project, self.filter)
            self.set_item_matched(project, matched);
            
class ProjectCompletionFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
    def begin_project (self, project):
        self.begin_item(project)
        if not project.attribs['matched_filter'] and self.filter != None:
            matched = self.match_completed(project, self.filter)
            self.set_item_matched(project, matched);

class TaskCompletionFilterVisitor(BaseFilterVisitor):
    def __init__(self, filtr, include=True):
        BaseFilterVisitor.__init__(self, include)
        self.filter = filtr
    def begin_task (self, task):
        self.begin_item(task)
        if not task.attribs['matched_filter'] and self.filter != None:
            matched = self.match_completed(task, self.filter)
            self.set_item_matched(task, matched);

class FlatteningVisitor (Visitor):
    def __init__(self):
        self.projects = []
    def begin_project (self, project):
        self.projects.append(project)
    def end_task (self, task):
        mypos = task.parent.children.index (task)
        for child in task.children:
            task.parent.children.insert (mypos, child)
            child.parent = task.parent
        task.children = []
        
class TaskCompletionSortingVisitor (Visitor):
    def end_project (self, project):
        project.children.sort(key=lambda item:self.get_key(item))
    def get_key (self, item):
        if item.date_completed != None:
            return item.date_completed
        return datetime.today()
    
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