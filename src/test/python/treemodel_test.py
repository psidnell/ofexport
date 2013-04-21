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

from treemodel import Task, Project, Folder, Context, Visitor, traverse, traverse_list, sort
import unittest

class DemoVisitor(Visitor):
    def __init__(self):
        self.tasks_started = []
        self.tasks_ended = []
        self.projects_started = []
        self.projects_ended = []
        self.folders_started = []
        self.folders_ended = []
        self.contexts_started = []
        self.contexts_ended = []
    def begin_task (self, task):
        self.tasks_started.append(task)
    def end_task (self, task):
        self.tasks_ended.append(task)
    def begin_project (self, project):
        self.projects_started.append(project)
    def end_project (self, project):
        self.projects_ended.append(project)
    def begin_folder (self, folder):
        self.folders_started.append(folder)
    def end_folder (self, folder):
        self.folders_ended.append(folder)
    def begin_context (self, context):
        self.contexts_started.append(context)
    def end_context (self, context):
        self.contexts_ended.append(context)

class SortableTask(Task):
    def get_sort_key(self):
        return self.name

class Test_treemodel(unittest.TestCase):
    
    def test_traverse_list_tasks (self):
        n1 = Task (name=u'n1')
        n2 = Task (name=u'n2')
        nodes = [n1,n2]
        visitor = DemoVisitor ()
        traverse_list (visitor, nodes)
        self.assertEqual(2, len(visitor.tasks_started))
        self.assertTrue(n1 in visitor.tasks_started)
        self.assertTrue(n2 in visitor.tasks_started)
        
        self.assertEqual(2, len(visitor.tasks_ended))
        self.assertTrue(n1 in visitor.tasks_ended)
        self.assertTrue(n2 in visitor.tasks_ended)
        
        self.assertEqual(0, len(visitor.projects_started))
        self.assertEqual(0, len(visitor.folders_started))
        self.assertEqual(0, len(visitor.contexts_started))
        
    def test_traverse_list_projects (self):
        n1 = Project (name=u'n1')
        n2 = Project (name=u'n2')
        nodes = [n1,n2]
        visitor = DemoVisitor ()
        traverse_list (visitor, nodes)
        self.assertEqual(2, len(visitor.projects_started))
        self.assertTrue(n1 in visitor.projects_started)
        self.assertTrue(n2 in visitor.projects_started)
        
        self.assertEqual(2, len(visitor.projects_ended))
        self.assertTrue(n1 in visitor.projects_ended)
        self.assertTrue(n2 in visitor.projects_ended)
        
        self.assertEqual(0, len(visitor.tasks_started))
        self.assertEqual(0, len(visitor.folders_started))
        self.assertEqual(0, len(visitor.contexts_started))
        
    def test_traverse_list_folders (self):
        n1 = Folder (name=u'n1')
        n2 = Folder (name=u'n2')
        nodes = [n1,n2]
        visitor = DemoVisitor ()
        traverse_list (visitor, nodes)
        self.assertEqual(2, len(visitor.folders_started))
        self.assertTrue(n1 in visitor.folders_started)
        self.assertTrue(n2 in visitor.folders_started)
        
        self.assertEqual(2, len(visitor.folders_ended))
        self.assertTrue(n1 in visitor.folders_ended)
        self.assertTrue(n2 in visitor.folders_ended)
        
        self.assertEqual(0, len(visitor.tasks_started))
        self.assertEqual(0, len(visitor.projects_started))
        self.assertEqual(0, len(visitor.contexts_started))
        
    def test_traverse_list_contexts (self):
        n1 = Context (name=u'n1')
        n2 = Context (name=u'n2')
        nodes = [n1,n2]
        visitor = DemoVisitor ()
        traverse_list (visitor, nodes)
        self.assertEqual(2, len(visitor.contexts_started))
        self.assertTrue(n1 in visitor.contexts_started)
        self.assertTrue(n2 in visitor.contexts_started)
        
        self.assertEqual(2, len(visitor.contexts_ended))
        self.assertTrue(n1 in visitor.contexts_ended)
        self.assertTrue(n2 in visitor.contexts_ended)
        
        self.assertEqual(0, len(visitor.tasks_started))
        self.assertEqual(0, len(visitor.projects_started))
        self.assertEqual(0, len(visitor.folders_started))
        
    def test_traverse_task (self):
        parent = Task (name=u'p')
        n1 = Task (name=u'n1')
        n2 = Task (name=u'n2')
        parent.children.append (n1)
        parent.children.append (n2)
        
        visitor = DemoVisitor ()
        traverse (visitor, parent)
        self.assertEqual(3, len(visitor.tasks_started))
        self.assertTrue(parent in visitor.tasks_started)
        self.assertTrue(n1 in visitor.tasks_started)
        self.assertTrue(n2 in visitor.tasks_started)
        
        self.assertEqual(3, len(visitor.tasks_ended))
        self.assertTrue(parent in visitor.tasks_ended)
        self.assertTrue(n1 in visitor.tasks_ended)
        self.assertTrue(n2 in visitor.tasks_ended)
        
    def test_traverse_task_when_not_marked (self):
        parent = Task (name=u'p')
        n1 = Task (name=u'n1')
        n2 = Task (name=u'n2')
        parent.children.append (n1)
        parent.children.append (n2)
        parent.marked = False
        
        visitor = DemoVisitor ()
        traverse (visitor, parent)
        self.assertEqual(0, len(visitor.tasks_started))
        self.assertEqual(0, len(visitor.tasks_ended))
        
    def test_traverse_project (self):
        parent = Project (name=u'p')
        n1 = Task (name=u'n1')
        n2 = Task (name=u'n2')
        parent.children.append (n1)
        parent.children.append (n2)
        
        visitor = DemoVisitor ()
        traverse (visitor, parent)
        self.assertEqual(2, len(visitor.tasks_started))
        self.assertEqual(1, len(visitor.projects_started))
        self.assertTrue(parent in visitor.projects_started)
        self.assertTrue(n1 in visitor.tasks_started)
        self.assertTrue(n2 in visitor.tasks_started)
        
        self.assertEqual(2, len(visitor.tasks_ended))
        self.assertEqual(1, len(visitor.projects_ended))
        self.assertTrue(parent in visitor.projects_ended)
        self.assertTrue(n1 in visitor.tasks_ended)
        self.assertTrue(n2 in visitor.tasks_ended)
        
    def test_traverse_project_when_not_marked (self):
        parent = Project (name=u'p')
        n1 = Task (name=u'n1')
        n2 = Task (name=u'n2')
        parent.children.append (n1)
        parent.children.append (n2)
        parent.marked = False
        
        visitor = DemoVisitor ()
        traverse (visitor, parent)
        self.assertEqual(0, len(visitor.tasks_started))
        self.assertEqual(0, len(visitor.projects_started))
        self.assertEqual(0, len(visitor.tasks_ended))
        self.assertEqual(0, len(visitor.projects_ended))
        
    def test_traverse_context (self):
        parent = Context (name=u'p')
        n1 = Task (name=u'n1')
        n2 = Task (name=u'n2')
        parent.children.append (n1)
        parent.children.append (n2)
        
        visitor = DemoVisitor ()
        traverse (visitor, parent)
        self.assertEqual(2, len(visitor.tasks_started))
        self.assertEqual(1, len(visitor.contexts_started))
        self.assertTrue(parent in visitor.contexts_started)
        self.assertTrue(n1 in visitor.tasks_started)
        self.assertTrue(n2 in visitor.tasks_started)
        
        self.assertEqual(2, len(visitor.tasks_ended))
        self.assertEqual(1, len(visitor.contexts_ended))
        self.assertTrue(parent in visitor.contexts_ended)
        self.assertTrue(n1 in visitor.tasks_ended)
        self.assertTrue(n2 in visitor.tasks_ended)
        
    def test_traverse_context_when_not_marked (self):
        parent = Context (name=u'p')
        n1 = Task (name=u'n1')
        n2 = Task (name=u'n2')
        parent.children.append (n1)
        parent.children.append (n2)
        parent.marked = False
        
        visitor = DemoVisitor ()
        traverse (visitor, parent)
        self.assertEqual(0, len(visitor.tasks_started))
        self.assertEqual(0, len(visitor.contexts_started))
        self.assertEqual(0, len(visitor.tasks_ended))
        self.assertEqual(0, len(visitor.contexts_ended))
        
    def test_traverse_folder (self):
        parent = Folder (name=u'p')
        n1 = Project (name=u'n1')
        n2 = Folder (name=u'n2')
        parent.children.append (n1)
        parent.children.append (n2)
        
        visitor = DemoVisitor ()
        traverse (visitor, parent)
        self.assertEqual(2, len(visitor.folders_started))
        self.assertEqual(1, len(visitor.projects_started))
        self.assertTrue(parent in visitor.folders_started)
        self.assertTrue(n1 in visitor.projects_started)
        self.assertTrue(n2 in visitor.folders_started)
        
        self.assertEqual(2, len(visitor.folders_ended))
        self.assertEqual(1, len(visitor.projects_ended))
        self.assertTrue(parent in visitor.folders_ended)
        self.assertTrue(n1 in visitor.projects_ended)
        self.assertTrue(n2 in visitor.folders_ended)
        
    def test_sort_no_key_defined (self):
        parent = Task (name=u'p')
        n1 = Task (name=u'n1')
        n2 = Task (name=u'n2')
        parent.children.append (n1)
        parent.children.append (n2)
        
        try:
            sort ([parent])
            self.fail('exception expected')
        except Exception as e:
            self.assertEquals("not implemented in <class 'treemodel.Task'>", e.message)
        
    def test_sort_order_when_sorted (self):
        parent = SortableTask (name=u'p')
        n1 = SortableTask (name=u'n1')
        n2 = SortableTask (name=u'n2')
        parent.children.append (n1)
        parent.children.append (n2)
        
        sort ([parent])
        
        self.assertEqual(n1, parent.children[0])
        self.assertEqual(n2, parent.children[1])
        
    def test_sort_order_when_unsorted (self):
        parent = SortableTask (name=u'p')
        n2 = SortableTask (name=u'n2')
        n1 = SortableTask (name=u'n1')
        parent.children.append (n1)
        parent.children.append (n2)
        
        sort ([parent])
        
        self.assertEqual(n1, parent.children[0])
        self.assertEqual(n2, parent.children[1])
        
        