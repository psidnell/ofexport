import unittest
from visitors import FolderNameFilterVisitor, TaskNameFilterVisitor, ProjectNameFilterVisitor, ContextNameFilterVisitor
from treemodel import Folder, Task, Project, Context, traverse_list, traverse
from datetime import datetime

class Test_visitors(unittest.TestCase):
    
    def test_FolderNameFilterVisitor_include (self):
        n1 = Folder (name=u'n1')
        n2 = Folder (name=u'n2 xxx')
        nodes = [n1, n2]
        visitor = FolderNameFilterVisitor ('xxx')
        traverse_list (visitor, nodes)
        self.assertFalse(n1.marked)
        self.assertTrue(n2.marked)
        
    def test_FolderNameFilterVisitor_exclude (self):
        n1 = Folder (name=u'n1')
        n2 = Folder (name=u'n2 xxx')
        nodes = [n1, n2]
        visitor = FolderNameFilterVisitor ('xxx', include=False)
        traverse_list (visitor, nodes)
        self.assertTrue(n1.marked)
        self.assertFalse(n2.marked)
        
    def test_FolderNameFilterVisitor_include_ignores_children (self):
        n1 = Folder (name=u'n1 xxx')
        n2 = Folder (name=u'n2')
        n1.add_child(n2)
        
        visitor = FolderNameFilterVisitor ('xxx')
        traverse (visitor, n1)
        self.assertTrue(n1.marked)
        self.assertTrue(n2.marked)
        
    def test_TaskNameFilterVisitor_include (self):
        n1 = Task (name=u'n1')
        n2 = Task (name=u'n2 xxx')
        nodes = [n1, n2]
        visitor = TaskNameFilterVisitor ('xxx')
        traverse_list (visitor, nodes)
        self.assertFalse(n1.marked)
        self.assertTrue(n2.marked)
        
    def test_TaskNameFilterVisitor_exclude (self):
        n1 = Task (name=u'n1')
        n2 = Task (name=u'n2 xxx')
        nodes = [n1, n2]
        visitor = TaskNameFilterVisitor ('xxx', include=False)
        traverse_list (visitor, nodes)
        self.assertTrue(n1.marked)
        self.assertFalse(n2.marked)
        
    def test_TaskNameFilterVisitor_include_ignores_children (self):
        n1 = Task (name=u'n1 xxx')
        n2 = Task (name=u'n2')
        n1.add_child(n2)
        
        visitor = TaskNameFilterVisitor ('xxx')
        traverse (visitor, n1)
        self.assertTrue(n1.marked)
        self.assertTrue(n2.marked)
        
    def test_ProjectNameFilterVisitor_include (self):
        n1 = Project (name=u'n1')
        n2 = Project (name=u'n2 xxx')
        nodes = [n1, n2]
        visitor = ProjectNameFilterVisitor ('xxx')
        traverse_list (visitor, nodes)
        self.assertFalse(n1.marked)
        self.assertTrue(n2.marked)
        
    def test_ProjectNameFilterVisitor_exclude (self):
        n1 = Project (name=u'n1')
        n2 = Project (name=u'n2 xxx')
        nodes = [n1, n2]
        visitor = ProjectNameFilterVisitor ('xxx', include=False)
        traverse_list (visitor, nodes)
        self.assertTrue(n1.marked)
        self.assertFalse(n2.marked)
        
    def test_ProjectNameFilterVisitor_include_ignores_children (self):
        n1 = Project (name=u'n1 xxx')
        n2 = Task (name=u'n2')
        n1.add_child(n2)
        
        visitor = ProjectNameFilterVisitor ('xxx')
        traverse (visitor, n1)
        self.assertTrue(n1.marked)
        self.assertTrue(n2.marked)

    def test_ContextNameFilterVisitor_include (self):
        n1 = Context (name=u'n1')
        n2 = Context (name=u'n2 xxx')
        nodes = [n1, n2]
        visitor = ContextNameFilterVisitor ('xxx')
        traverse_list (visitor, nodes)
        self.assertFalse(n1.marked)
        self.assertTrue(n2.marked)
        
    def test_ContextNameFilterVisitor_exclude (self):
        n1 = Context (name=u'n1')
        n2 = Context (name=u'n2 xxx')
        nodes = [n1, n2]
        visitor = ContextNameFilterVisitor ('xxx', include=False)
        traverse_list (visitor, nodes)
        self.assertTrue(n1.marked)
        self.assertFalse(n2.marked)
        
    def test_ContextNameFilterVisitor_include_ignores_children (self):
        n1 = Context (name=u'n1 xxx')
        n2 = Context (name=u'n2')
        n1.add_child(n2)
        
        visitor = ContextNameFilterVisitor ('xxx')
        traverse (visitor, n1)
        self.assertTrue(n1.marked)
        self.assertTrue(n2.marked)
