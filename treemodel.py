from datetime import datetime
from typeof import TypeOf

TASK = 'Task'
PROJECT = 'Project'
CONTEXT = 'Context'
FOLDER = 'Folder'

class NodeFwdDecl (object):
    # How to do forward class declarations in python?
    pass

class Node (NodeFwdDecl):
    name = TypeOf ('name', unicode)
    parent = TypeOf ('parent', NodeFwdDecl)
    marked = TypeOf ('marked', bool)
    children = TypeOf ('children', list)
    attribs = TypeOf ('attribs', dict)
    type = TypeOf ('type', str)
    
    def __init__ (self, nType,
                  name=None,
                  parent=None,
                  marked=True,
                  children=[],
                  attribs = {}):
        self.name = name
        self.parent = parent
        self.children = list(children)
        self.marked = marked
        self.attribs = dict(attribs)
        self.type = nType
    def add_child (self, child):
        self.children.append(child)
        child.parent = self
    def get_sort_key (self):
        raise Exception ('not implemented in ' + str (self.__class__))
    def __str__ (self):
        return self.name

class Context(Node):
    def __init__ (self,
                  name=None,
                  parent=None,
                  marked=True,
                  children=[],
                  attribs = {}):
        Node.__init__ (self, CONTEXT,
                       name=name,
                       parent=parent,
                       marked=marked,
                       children=children,
                       attribs=attribs)
        
class Task(Node):
    flagged = TypeOf ('flagged', bool)
    context = TypeOf ('context', Context)
    date_completed = TypeOf ('date_completed', datetime)
    date_to_start = TypeOf ('date_to_start', datetime)
    date_due = TypeOf ('date_due', datetime)
    
    def __init__ (self,
                  name=None,
                  parent=None,
                  marked=True,
                  flagged=False,
                  children=[],
                  context=None,
                  attribs={},
                  date_completed=None,
                  date_to_start=None,
                  date_due=None):
        Node.__init__ (self, TASK,
                       name=name,
                       parent=parent,
                       marked=marked,
                       children=children,
                       attribs=attribs)
        self.flagged = flagged
        self.context = context
        self.date_completed = date_completed
        self.date_to_start = date_to_start
        self.date_due = date_due

class Folder(Node):
    def __init__ (self,
                  name=None,
                  parent=None,
                  marked=True,
                  children=[],
                  attribs = {}):
        Node.__init__ (self, FOLDER,
                       name=name,
                       parent=parent,
                       marked=marked,
                       children=children,
                       attribs=attribs)
class Project(Node):
    flagged = TypeOf ('flagged', bool)
    date_completed = TypeOf ('date_completed', datetime)
    folder = TypeOf ('folder', Folder)
    def __init__ (self,
                   name=None,
                  parent=None,
                  marked=True,
                  children=[],
                  attribs = {},
                  flagged = False,
                  date_completed=None,
                  folder=None):
        Node.__init__ (self, PROJECT,
                       name=name,
                       parent=parent,
                       marked=marked,
                       children=children,
                       attribs=attribs)
        self.flagged = flagged
        self.date_completed = date_completed
        self.folder = folder
    
class Visitor(object):
    def begin_any (self, item):
        pass
    def end_any (self, item):
        pass
    def begin_folder (self, folder):
        pass
    def end_folder (self, folder):
        pass
    def begin_project (self, project):
        pass
    def end_project (self, project):
        pass
    def begin_task (self, task):
        pass
    def end_task (self, task):
        pass
    def begin_context (self, context):
        pass
    def end_context (self, context):
        pass

def sort (items):
    for child in items:
        child.children.sort(key=lambda item:item.get_sort_key ())
        sort(child.children)

def traverse_list (visitor, lst, ignore_marked=False):
    for item in lst:
        traverse (visitor, item, ignore_marked = ignore_marked)

def traverse (visitor, item, ignore_marked=False):       
    if item.type == FOLDER:
        traverse_folder (visitor, item, ignore_marked = ignore_marked)
    elif item.type == CONTEXT:
        traverse_context (visitor, item, ignore_marked = ignore_marked)
    elif item.type == PROJECT:
        traverse_project (visitor, item, ignore_marked = ignore_marked)
    elif item.type == TASK:
        traverse_task (visitor, item, ignore_marked = ignore_marked)

def traverse_context (visitor, context, ignore_marked=False):
    if context.marked or ignore_marked:
        visitor.begin_any (context)
        visitor.begin_context (context)
        if context.marked or ignore_marked: # it might have been unmarked in begin_...
            traverse_list (visitor, context.children, ignore_marked = ignore_marked)
        visitor.end_context (context) # must match calls to begin_...
        visitor.end_any (context)

def traverse_task (visitor, task, ignore_marked=False):
    if task.marked or ignore_marked:
        visitor.begin_any (task)
        visitor.begin_task (task)
        if task.marked or ignore_marked: # it might have been unmarked in begin_...
            traverse_list (visitor, task.children, ignore_marked = ignore_marked)
        visitor.end_task (task) # must match calls to begin_...
        visitor.end_any (task)
    
def traverse_project (visitor, project,ignore_marked=False):
    if project.marked or ignore_marked:
        visitor.begin_any (project)
        visitor.begin_project (project)
        if project.marked or ignore_marked: # it might have been unmarked in begin_...
            traverse_list (visitor, project.children, ignore_marked = ignore_marked)
        visitor.end_project (project) # must match calls to begin_...
        visitor.end_any (project)
    
def traverse_folder (visitor, folder, ignore_marked=False):
    if folder.marked or ignore_marked:
        visitor.begin_any (folder)
        visitor.begin_folder(folder)
        if folder.marked or ignore_marked: # it might have been unmarked in begin_...
            traverse_list (visitor, folder.children, ignore_marked = ignore_marked)
        visitor.end_folder (folder) # must match calls to begin_...
        visitor.end_any (folder)