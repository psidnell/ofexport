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
    date_completed = TypeOf ('date_completed', datetime)
    folder = TypeOf ('folder', Folder)
    def __init__ (self,
                   name=None,
                  parent=None,
                  marked=True,
                  children=[],
                  attribs = {},
                  date_completed=None,
                  folder=None):
        Node.__init__ (self, PROJECT,
                       name=name,
                       parent=parent,
                       marked=marked,
                       children=children,
                       attribs=attribs)
        self.date_completed = date_completed
        self.folder = folder
    
class Visitor(object):
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

def traverse_list (visitor, lst, only_marked=True):
    for item in lst:
        if item.type == FOLDER:
            traverse_folder (visitor, item, only_marked = only_marked)
        elif item.type == CONTEXT:
            traverse_context (visitor, item, only_marked = only_marked)
        elif item.type == PROJECT:
            traverse_project (visitor, item, only_marked = only_marked)
        elif item.type == TASK:
            traverse_task (visitor, item, only_marked = only_marked)
            
def traverse_folders (visitor, folders, only_marked=True):
    traverse_list (visitor, folders, only_marked = only_marked)

def traverse_contexts (visitor, contexts, only_marked=True):
    traverse_list (visitor, contexts, only_marked = only_marked)

def traverse_context (visitor, context, only_marked=True):
    if context.marked or not only_marked:
        visitor.begin_context (context)
        traverse_list (visitor, context.children, only_marked = only_marked)
        visitor.end_context (context)

def traverse_task (visitor, task, only_marked=True):
    if task.marked or not only_marked:
        visitor.begin_task (task)
        traverse_list (visitor, task.children, only_marked = only_marked)
        visitor.end_task (task)
    
def traverse_project (visitor, project,only_marked=True):
    if project.marked or not only_marked:
        visitor.begin_project (project)
        traverse_list (visitor, project.children, only_marked = only_marked)
        visitor.end_project (project)
    
def traverse_folder (visitor, folder, only_marked=True):
    if folder.marked or not only_marked:
        visitor.begin_folder(folder)
        traverse_list (visitor, folder.children, only_marked = only_marked)
        visitor.end_folder (folder)