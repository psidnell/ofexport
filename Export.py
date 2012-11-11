import sqlite3
from pprint import pprint
from datetime import datetime

'''
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
'''




'''
TODO
- tasklist->children
- generic node class
- link objects properly
- sort tasks
- visitor pattern
- use select dateField(ZTIME, 'unixepoch', '+31 years') from ...
'''

THIRTY_ONE_YEARS = 60 * 60 * 24 * 365 * 31 + 60 * 60 * 24 * 8

class AttribDesc( object ):
    def __init__( self, name ):
        self._name = name
    def __get__( self, instance, owner ):
        return instance.__dict__[self._name]
    def __set__( self, instance, value ):
        instance.__dict__[self._name] = value
        
class TypedDesc(object):
    def __init__(self,name, exptype):
        self.name = name
        self.expected_type = exptype
    def __get__(self,obj,cls):
        if obj is None:
            return self
        else:
            return obj.__dict__[self.name]
    def __set__(self,obj,value):
        if not isinstance(value,self.expected_type):
            raise TypeError("Expected %s got %s" % (self.expected_type, value.__class__.__name__))
        obj.__dict__[self.name] = value
    def __delete__(self,obj):
        raise AttributeError("Can't delete")

class Node (object):
    name = TypedDesc ('name', unicode)
    parent = None
    def __init__ (self, attribs):
        self.__dict__.update (attribs)
    def __getitem__ (self, key):
        return self.__dict__[key]
    def __setitem__ (self, key, val):
        self.__dict__[key] = val
    def __contains__ (self, key):
        return key in self.__dict__


class Context(Node):
    TABLE='context'
    COLUMNS=['persistentIdentifier', 'name', 'parent', 'childrenCount']
    def __init__(self, param):
        Node.__init__(self,param)
        self.name=self.__dict__['name']

class Task(Node):
    TABLE='task'
    COLUMNS=['persistentIdentifier', 'name', 'dateDue', 'dateCompleted','projectInfo', 'context', 'containingProjectInfo', 'childrenCount', 'parent']
    context = TypedDesc('context', Context)
    def __init__(self, param):
        Node.__init__(self,param)
        self.name=self.__dict__['name']

class Folder(Node):
    TABLE='folder'
    COLUMNS=['persistentIdentifier', 'name', 'childrenCount', 'parent']
    def __init__(self, param):
        Node.__init__(self,param)
        self.name=self.__dict__['name']
        
class ProjectInfo(Node):
    TABLE='projectinfo'
    COLUMNS=['pk', 'folder']
    def __init__(self, param):
        Node.__init__(self,param)

class Project(Task):
    project_info = TypedDesc ('project_info', ProjectInfo)
    folder = TypedDesc ('folder', Folder)

    
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

def transmute_projects (project_infos, folders, tasks):
    '''
    Some tasks are actually projects, convert them
    '''
    projects = []
    for project in tasks.values():        
        if project['projectInfo'] != None:
            projects.append(project)
            project_info = project_infos[project['projectInfo']]
            project_info.name = project.name
            project.__class__ = Project
            
            # Wire the project to it's folder while we're here 
            if project_info['folder'] != None:
                folder = folders[project_info['folder']]
                project.folder = folder
                if not ('taskList' in folder):
                    folder['taskList'] = [project]
                else:
                    folder['taskList'].append(project)
    return projects

def wire_projects_and_folders (project_infos, folders, tasks):
    '''
    Some tasks are actually projects, convert them
    '''
    for project in tasks.values():        
        if project['projectInfo'] != None:
            project_info = project_infos[project['projectInfo']]
            project_info.name = project.name
            project.__class__ = Project
            
            # Wire the project to it's folder while we're here 
            if project_info['folder'] != None:
                folder = folders[project_info['folder']]
                project.folder = folder
                if not ('taskList' in folder):
                    folder['taskList'] = [project]
                else:
                    folder['taskList'].append(project)

def wire_task_hierarchy (tasks):
    for task in tasks.values():  
        if task['parent'] != None:
            parent = tasks[task['parent']]
            if not ('taskList' in parent):
                parent['taskList'] = [task]
            else:
                parent['taskList'].append(task)

def wire_tasks_to_enclosing_projects (project_infos, tasks):
    for task in tasks.values():  
        if task['containingProjectInfo'] != None:
            projectInfo = project_infos[task['containingProjectInfo']]
            task['projectName'] = projectInfo['name']
       
def wire_tasks_and_contexts (contexts, tasks):
    for task in tasks.values():  

        if task['context'] != None:
            context = contexts[task['context']]
            task.context = context
            if not ('taskList' in context):
                context['taskList'] = [task]
            else:
                context['taskList'].append(task)
            task['contextName'] = context['name']
            
def wire_folder_hierarchy (folders):
    for folder in folders.values():
        if folder['parent'] != None:
            parent = folders[folder['parent']]
            if not ('taskList' in parent):
                parent['taskList'] = [folder]
            else:
                parent['taskList'].append(folder)
                
def wire_context_hierarchy (contexts):
    for context in contexts.values():
        if context['parent'] != None:
            parent = contexts[context['parent']]
            if not ('taskList' in parent):
                parent['taskList'] = [context]
            else:
                parent['taskList'].append(context)

def printTree (depth, item):
    dateCompleted = ''
    if 'dateCompleted' in item and item['dateCompleted'] != None:
        dateCompleted = datetime.fromtimestamp(THIRTY_ONE_YEARS + item['dateCompleted'])
    context = ''
    if 'contextName' in item:
        context = item['contextName']
    project = ''
    if 'projectName' in item:
        project = item['projectName']
    print (' ' * (depth * 4)) + item['name'] + '[' + str(item['childrenCount']) + '] ' + item.__class__.__name__ + ' P:' + project + ' C:' + context + ' ' + str(dateCompleted)
    if 'taskList' in item:
        for subItem in item['taskList']:
            printTree(depth + 1, subItem)

def buildModel (db):
    conn = sqlite3.connect(db)
    contexts = query (conn, clazz=Context)
    project_infos = query (conn, clazz=ProjectInfo)
    folders = query (conn, clazz=Folder)
    tasks = query (conn, clazz=Task)
    
    projects = transmute_projects (project_infos, folders, tasks)
    wire_task_hierarchy(tasks)
    wire_tasks_to_enclosing_projects (project_infos, tasks)
    wire_tasks_and_contexts(contexts, tasks)
    wire_folder_hierarchy (folders)
    wire_context_hierarchy (contexts)
    
    conn.close ()
    
    return folders, projects, contexts, tasks

folders, projects, contexts, tasks = buildModel ('/Users/psidnell/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2')

'''
for folder in folders.values ():
    if folder['parent'] == None:
        printTree (0, folder)
for context in contexts.values ():
    if context['parent'] == None:
        printTree (0, context)
'''

for folder in folders.values ():
    if folder['parent'] == None and folder['name'] == 'Work':
        printTree (0, folder)
