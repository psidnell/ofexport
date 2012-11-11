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

def query (conn, table, columns):
    c = conn.cursor()
    results = {}
    for row in c.execute('SELECT ' + (','.join(columns)) + ' from ' + table):
        rowData = {}
        for i in range(0,len(columns)):
            key = columns[i]
            val = row[i]
            rowData[key] = val
        results[rowData[columns[0]]] = rowData
    c.close()
    return results

def knitProjectNames (projects, tasks):
    for task in tasks.values():        
        if task['projectInfo'] != None:
            projectInfo = projects[task['projectInfo']]
            projectInfo['name'] = task['name']

def knitTasks (projects, folders, contexts, tasks):
    for task in tasks.values():
        task['type'] = 'TASK'
        
        if task['parent'] != None:
            parent = tasks[task['parent']]
            if not ('taskList' in parent):
                parent['taskList'] = [task]
            else:
                parent['taskList'].append(task)
                
        if task['containingProjectInfo'] != None:
            projectInfo = projects[task['containingProjectInfo']]
            task['projectName'] = projectInfo['name']
        
        if task['projectInfo'] != None:
            task['type'] = 'PROJECT'
            projectInfo = projects[task['projectInfo']]
            if projectInfo['folder'] != None:
                folder = folders[projectInfo['folder']]
                if not ('taskList' in folder):
                    folder['taskList'] = [task]
                else:
                    folder['taskList'].append(task)
                    
        if task['context'] != None:
            context = contexts[task['context']]
            if not ('taskList' in context):
                context['taskList'] = [task]
            else:
                context['taskList'].append(task)
            task['contextName'] = context['name']
            
def knitFolders (folders):
    for folder in folders.values():
        folder['type'] = 'FOLDER'
        if folder['parent'] != None:
            parent = folders[folder['parent']]
            if not ('taskList' in parent):
                parent['taskList'] = [folder]
            else:
                parent['taskList'].append(folder)
                
def knitContexts (contexts):
    for context in contexts.values():
        context['type'] = 'CONTEXT'
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
    print (' ' * (depth * 4)) + item['name'] + '[' + str(item['childrenCount']) + '] ' + item['type'] + ' P:' + project + ' C:' + context + ' ' + str(dateCompleted)
    if 'taskList' in item:
        for subItem in item['taskList']:
            printTree(depth + 1, subItem)

def buildModel (db):
    conn = sqlite3.connect(db)

    columns=['persistentIdentifier', 'name', 'parent', 'childrenCount']
    contexts = query (conn, 'context', columns)
    
    columns=['pk', 'folder']
    projects = query (conn, 'projectinfo', columns)
    
    columns=['persistentIdentifier', 'name', 'childrenCount', 'parent']
    folders = query (conn, 'folder', columns)
    
    columns=['persistentIdentifier', 'name', 'dateDue', 'dateCompleted','projectInfo', 'context', 'containingProjectInfo', 'childrenCount', 'parent']
    tasks = query (conn, 'task', columns)
    
    knitProjectNames (projects, tasks)
    knitTasks(projects, folders, contexts, tasks)
    knitFolders (folders)
    knitContexts (contexts)
    
    conn.close ()
    
    return folders, contexts, tasks

folders, contexts, tasks = buildModel ('/Users/psidnell/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2')

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
