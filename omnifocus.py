import sqlite3
from datetime import date

'''
A library for loading a data model from the Omnifocus SQLite database.

---------
Notes on discovering what the Omni schema looks like

sqlite3 ~/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2

.tables
Attachment   Folder       Perspective  Setting    
Context      ODOMetadata  ProjectInfo  Task       

sqlite> .schema Task
CREATE TABLE Task (persistentIdentifier text NOT NULL PRIMARY KEY, blocked integer NOT NULL, blockedByFutureStartDate integer NOT NULL, 
childrenCount integer NOT NULL, childrenCountAvailable integer NOT NULL, childrenCountCompleted integer NOT NULL, completeWhenChildrenComplete integer NOT NULL,
containingProjectContainsSingletons integer NOT NULL, containingProjectInfo text, containsNextTask integer NOT NULL, context text, creationOrdinal integer,
dateAdded timestamp NOT NULL, dateCompleted timestamp, dateDue timestamp, dateModified timestamp NOT NULL, dateToStart timestamp, effectiveContainingProjectInfoActive integer NOT NULL,
effectiveContainingProjectInfoRemaining integer NOT NULL, effectiveDateDue timestamp, effectiveDateToStart timestamp, effectiveFlagged integer NOT NULL,
effectiveInInbox integer NOT NULL, estimatedMinutes integer, flagged integer NOT NULL, hasCompletedDescendant integer NOT NULL, hasFlaggedTaskInTree integer NOT NULL,
hasUnestimatedLeafTaskInTree integer NOT NULL, inInbox integer NOT NULL, isDueSoon integer NOT NULL, isOverdue integer NOT NULL, maximumEstimateInTree integer,
minimumEstimateInTree integer, name text, nextTaskOfProjectInfo text, noteXMLData blob, parent text, projectInfo text, rank integer NOT NULL, repetitionMethodString text,
repetitionRuleString text, sequential integer NOT NULL);
CREATE INDEX Task_containingProjectInfo on Task (containingProjectInfo);
CREATE INDEX Task_context on Task (context);
CREATE INDEX Task_nextTaskOfProjectInfo on Task (nextTaskOfProjectInfo);
CREATE INDEX Task_parent on Task (parent);
CREATE INDEX Task_projectInfo on Task (projectInfo);

.schema ProjectInfo
CREATE TABLE ProjectInfo (pk text NOT NULL PRIMARY KEY, containsSingletonActions integer NOT NULL, folder text, folderEffectiveActive integer NOT NULL,
lastReviewDate timestamp, minimumDueDate timestamp, nextReviewDate timestamp, nextTask text, numberOfAvailableTasks integer NOT NULL, numberOfDueSoonTasks integer NOT NULL,
numberOfOverdueTasks integer NOT NULL, numberOfRemainingTasks integer NOT NULL, reviewRepetitionString text, status text NOT NULL, task text, taskBlocked integer NOT NULL,
taskBlockedByFutureStartDate integer NOT NULL, taskDateToStart timestamp);
CREATE INDEX ProjectInfo_folder on ProjectInfo (folder);
CREATE INDEX ProjectInfo_nextTask on ProjectInfo (nextTask);
CREATE INDEX ProjectInfo_task on ProjectInfo (task);


sqlite> .schema Folder
CREATE TABLE Folder (persistentIdentifier text NOT NULL PRIMARY KEY, active integer NOT NULL, childrenCount integer NOT NULL, creationOrdinal integer,
dateAdded timestamp NOT NULL, dateModified timestamp NOT NULL, effectiveActive integer NOT NULL, name text, noteXMLData blob, numberOfAvailableTasks integer NOT NULL,
numberOfDueSoonTasks integer NOT NULL, numberOfOverdueTasks integer NOT NULL, parent text, rank integer NOT NULL);
CREATE INDEX Folder_parent on Folder (parent);


.schema Context
CREATE TABLE Context (persistentIdentifier text NOT NULL PRIMARY KEY, active integer NOT NULL, allowsNextAction integer NOT NULL, altitude real,
availableTaskCount integer NOT NULL, childrenCount integer NOT NULL, creationOrdinal integer, dateAdded timestamp NOT NULL, dateModified timestamp NOT NULL,
effectiveActive integer NOT NULL, latitude real, localNumberOfDueSoonTasks integer NOT NULL, localNumberOfOverdueTasks integer NOT NULL, locationName text,
longitude real, name text, noteXMLData blob, notificationFlags integer, parent text, radius real, rank integer NOT NULL, remainingTaskCount integer NOT NULL,
totalNumberOfDueSoonTasks integer NOT NULL, totalNumberOfOverdueTasks integer NOT NULL);
CREATE INDEX Context_parent on Context (parent);

.schema Perspective (no name!!!)

CREATE TABLE Perspective (persistentIdentifier text NOT NULL PRIMARY KEY, creationOrdinal integer, dateAdded timestamp NOT NULL, dateModified timestamp NOT NULL, valueData blob);
'''

THIRTY_ONE_YEARS = 60 * 60 * 24 * 365 * 31 + 60 * 60 * 24 * 8

class AttribDesc(object):
    def __init__(self, name):
        self._name = name
    def __get__(self, instance, owner):
        return instance.attribs[self._name]
    def __set__(self, instance, value):
        instance.attribs[self._name] = value
        
class TypedDesc(object):
    def __init__(self,name, exptype, value=None):
        self.name = name
        self.expected_type = exptype
    def __get__(self,obj,cls):
        if obj is None:
            return self
        else:
            return obj.__dict__[self.name]
    def __set__(self,obj,value):
        if not (isinstance(value,self.expected_type) or value == None):
            raise TypeError("Expected %s got %s" % (self.expected_type, value.__class__.__name__))
        obj.__dict__[self.name] = value
    def __delete__(self,obj):
        raise AttributeError("Can't delete")

class DateAttribDesc (AttribDesc):
    def __init__( self, name ):
        AttribDesc.__init__(self, name)
    def __get__(self,obj,cls):
        val = AttribDesc.__get__(self, obj, cls)
        if val == None:
            return None
        return date.fromtimestamp(THIRTY_ONE_YEARS + val)

class BoolAttribDesc (AttribDesc):
    def __init__( self, name ):
        AttribDesc.__init__(self, name)
    def __get__(self,obj,cls):
        val = AttribDesc.__get__(self, obj, cls)
        if val == None:
            return None
        return bool(val)
    
class IntAttribDesc (AttribDesc):
    def __init__( self, name ):
        AttribDesc.__init__(self, name)
    def __get__(self,obj,cls):
        val = AttribDesc.__get__(self, obj, cls)
        if val == None:
            return None
        return int(val)

class UnicodeAttribDesc (AttribDesc):
    def __init__( self, name ):
        AttribDesc.__init__(self, name)
    def __get__(self,obj,cls):
        val = AttribDesc.__get__(self, obj, cls)
        if val == None:
            return None
        return val
           
class Node (object):
    def __init__ (self, attribs):
        self.attribs = attribs
        self.children = []
    def __getitem__ (self, key):
        return self.attribs[key]
    def __contains__ (self, key):
        return key in self.attribs

class Context(Node):
    TABLE='context'
    COLUMNS=['persistentIdentifier', 'name', 'parent', 'childrenCount', 'rank']
    name = TypedDesc ('name', unicode)
    rank = IntAttribDesc ('rank')
    persistent_identifier = AttribDesc ('persistentIdentifier')
    def __init__(self, param):
        Node.__init__(self,param)
        self.name=self.attribs['name']
        self.parent = None
    def __str__ (self):
        return self.name

class Task(Node):
    TABLE='task'
    COLUMNS=['persistentIdentifier', 'name', 'dateDue', 'dateCompleted','dateToStart', 'dateDue', 
             'projectInfo', 'context', 'containingProjectInfo', 'childrenCount', 'parent', 'rank',
             'flagged', 'noteXMLData']
    name = UnicodeAttribDesc ('name')
    date_completed = DateAttribDesc ('dateCompleted')
    date_to_start = DateAttribDesc ('dateToStart')
    date_due = DateAttribDesc ('dateDue')
    flagged = BoolAttribDesc ('flagged')
    context = TypedDesc('context', Context)
    note = UnicodeAttribDesc ('noteXMLData')
    rank = IntAttribDesc ('rank')
    persistent_identifier = AttribDesc ('persistentIdentifier')
    def __init__(self, param):
        Node.__init__(self,param)
        self.name=self.attribs['name']
        self.parent = None
        self.context = None
    def __str__ (self):
        return self.name

class Folder(Node):
    TABLE='folder'
    COLUMNS=['persistentIdentifier', 'name', 'childrenCount', 'parent', 'rank', 'noteXMLData']
    name = TypedDesc ('name', unicode)
    note = UnicodeAttribDesc ('noteXMLData')
    rank = IntAttribDesc ('rank')
    persistent_identifier = AttribDesc ('persistentIdentifier')
    def __init__(self, param):
        Node.__init__(self,param)
        self.name=self.attribs['name']
        self.parent = None
    def __str__ (self):
        return self.name
        
class ProjectInfo(Node):
    TABLE='projectinfo'
    COLUMNS=['pk', 'folder']
    def __init__(self, param):
        Node.__init__(self,param)

class Project(Task):
    project_info = TypedDesc ('project_info', ProjectInfo)
    folder = TypedDesc ('folder', Folder)
    def __init__(self):
        self.folder = None
    def __str__ (self):
        return self.name

def query (conn, clazz):
    c = conn.cursor()
    columns = clazz.COLUMNS
    results = {}
    for row in c.execute('SELECT ' + (','.join(columns)) + ' from ' + clazz.TABLE):
        rowData = {}
        for i in range(0,len(columns)):
            key = columns[i]
            val = row[i]
            rowData[key] = val
        node = clazz (rowData)
        results[rowData[columns[0]]] = node
    c.close()
    return results

def transmute_projects (project_infos, tasks):
    '''
    Some tasks are actually projects, convert them
    '''
    projects = {}
    for project in tasks.values():        
        if project['projectInfo'] != None:
            projects[project['persistentIdentifier']] = project
            project_info = project_infos[project['projectInfo']]
            project.project_info = project_info
            project.__class__ = Project
            project.__init__()
            project_info.project = project
    return projects

def wire_projects_and_folders (projects, folders):
    '''
    Some tasks are actually projects, convert them
    '''
    for project in projects.values():        
        if project['projectInfo'] != None:
            project_info = project.project_info
            if project_info['folder'] != None:
                folder = folders[project_info['folder']]
                project.folder = folder
                folder.children.append(project)

def wire_task_hierarchy (tasks):
    for task in tasks.values():  
        if task['parent'] != None:
            parent = tasks[task['parent']]
            parent.children.append(task);
            task.parent = parent
            
def wire_tasks_to_enclosing_projects (project_infos, tasks):
    for task in tasks.values():  
        if task['containingProjectInfo'] != None:
            project_info = project_infos[task['containingProjectInfo']]
            project = project_info.project
            task.project = project
       
def wire_tasks_and_contexts (contexts, tasks):
    for task in tasks.values():  
        if task['context'] != None:
            context = contexts[task['context']]
            task.context = context
            context.children.append(task)
            
def wire_folder_hierarchy (folders):
    for folder in folders.values():
        if folder['parent'] != None:
            parent = folders[folder['parent']]
            parent.children.append (folder)
            folder.parent = parent
                
def wire_context_hierarchy (contexts):
    for context in contexts.values():
        if context['parent'] != None:
            parent = contexts[context['parent']]
            parent.children.append(context)
            context.parent = parent

def printTree (depth, item):
    print (' ' * (depth * 4)) + str(item['rank']) + ':' + str(item)
    for subItem in item.children:
        printTree(depth + 1, subItem)
        
def sort (items):
    for child in items:
        child.children.sort(key=lambda item:item['rank'])
        sort(child.children)

def only_roots (items):
    roots = []
    for item in items:
        if item.parent == None:
            roots.append(item)
    return roots

def build_model (db):
    conn = sqlite3.connect(db)
    contexts = query (conn, clazz=Context)
    project_infos = query (conn, clazz=ProjectInfo)
    folders = query (conn, clazz=Folder)
    tasks = query (conn, clazz=Task)
    
    projects = transmute_projects (project_infos, tasks)
    wire_projects_and_folders(projects, folders)
    wire_task_hierarchy(tasks)
    wire_tasks_to_enclosing_projects (project_infos, tasks)
    wire_tasks_and_contexts(contexts, tasks)
    wire_folder_hierarchy (folders)
    wire_context_hierarchy (contexts)
    
    conn.close ()
    
    folder_roots = only_roots (folders.values())
    context_roots = only_roots (contexts.values())
    
    sort(folder_roots)
    sort(context_roots)
    
    return folder_roots, context_roots

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

def traverse_folders (visitor, folders):
    for folder in folders:
        traverse_folder (visitor, folder)

def traverse_contexts (visitor, contexts):
    for context in contexts:
        traverse_context (visitor, context)

def traverse_context (visitor, context):
    visitor.begin_context (context)
    for child in context.children:
        if child.__class__ == Context:
            traverse_context (visitor, child)
        elif child.__class__ == Project:
            traverse_project (visitor, child)
        else:
            traverse_task (visitor, child)
    visitor.end_context (context)

def traverse_task (visitor, task):
    visitor.begin_task (task)
    for subtask in task.children:
        traverse_task (visitor, subtask)
    visitor.end_task (task)
    
def traverse_project (visitor, project):
    visitor.begin_project (project)
    for task in project.children:
        traverse_task (visitor, task)
    visitor.end_project (project)
    
def traverse_folder (visitor, folder):
    visitor.begin_folder(folder)
    for child in folder.children:
        if child.__class__ == Folder:
            traverse_folder (visitor, child)
        else:
            traverse_project (visitor, child)
    visitor.end_folder (folder)
    
class PrintingVisitor(Visitor):
    def __init__ (self, indent=4):
        self.depth = 0
        self.indent = indent
    def begin_folder (self, folder):
        print self.spaces() + '* Folder: ' + folder.name
        print self.spaces () + '  - Note: ' + str(folder.note)
        self.depth+=1
    def end_folder (self, folder):
        self.depth-=1
    def begin_project (self, project):
        print self.spaces () + '* Project: ' + str(project)
        self.print_task_attribs (project);
        self.depth+=1
    def end_project (self, project):
        self.depth-=1
    def begin_task (self, task):
        print self.spaces() + '* Task: ' + task.name
        self.print_task_attribs (task);
        self.depth+=1
    def end_task (self, task):
        self.depth-=1
    def begin_context (self, context):
        print self.spaces() + '* Context: ' + context.name
        self.depth+=1
    def end_context (self, context):
        self.depth-=1
    def print_task_attribs (self, task):
        # Tasks and projects have same attribs
        print self.spaces () + '  - Context: ' + str(task.context)
        print self.spaces () + '  - DateCompleted: ' + str(task.date_completed)
        print self.spaces () + '  - StartDate: ' + str(task.date_to_start)
        print self.spaces () + '  - Due: ' + str(task.date_due)
        print self.spaces () + '  - Flagged: ' + str(task.flagged)
        print self.spaces () + '  - Note: ' + str(task.note)
    def spaces (self):
        return ' ' * self.depth * self.indent

