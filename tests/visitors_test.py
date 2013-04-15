import unittest
from visitors import FolderNameFilterVisitor, TaskNameFilterVisitor, ProjectNameFilterVisitor, ContextNameFilterVisitor
from treemodel import Folder, Task, Project, Context, traverse_list, traverse

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
    
    def test_Scenario_1 (self):
        '''
        In project mode select a single deeply nested task for inclusion
        '''
        f_on_path = Folder (name='1')
        p_on_path = Project (name='2', parent=f_on_path)
        t1_on_path = Task (name='3', parent=p_on_path)
        t2_selected = Task (name='xxx', parent=t1_on_path)
        t3_on_path = Task (name='5', parent=t2_selected)
        t4 = Task (name='3', parent=t1_on_path)
        
        f = Folder (name='1', parent=f_on_path)
        p = Project (name='2', parent=f)
        t1 = Task (name='3', parent=p)
        t2 = Task (name='3', parent=t1)
        t3 = Task (name='5', parent=t2)
        
        c1 = Context (name='6')
        c1.add_child(t2_selected)
        
        c2 = Context (name='7')
        c2.add_child(t3)
        
        traverse_list (TaskNameFilterVisitor ('xxx'), [f_on_path])
        
        self.assertTrue(f_on_path.marked)
        self.assertTrue(p_on_path.marked)
        self.assertTrue(t1_on_path.marked)
        self.assertTrue(t2_selected.marked)
        self.assertTrue(t3_on_path.marked)
        
        self.assertTrue(c1.marked)
        self.assertTrue(c2.marked)
        
        self.assertFalse(f.marked)
        self.assertFalse(p.marked)
        self.assertFalse(t1.marked)
        self.assertFalse(t2.marked)
        self.assertFalse(t3.marked)
        self.assertFalse(t4.marked)
        
    def test_Scenario_2 (self):
        '''
        In project mode select a single deeply nested task for exclusion
        '''
        f_on_path = Folder (name='1')
        p_on_path = Project (name='2', parent=f_on_path)
        t1_on_path = Task (name='3', parent=p_on_path)
        t2_selected = Task (name='xxx', parent=t1_on_path)
        t3_on_path = Task (name='5', parent=t2_selected)
        t4 = Task (name='3', parent=t1_on_path)
        
        f = Folder (name='1', parent=f_on_path)
        p = Project (name='2', parent=f)
        t1 = Task (name='3', parent=p)
        t2 = Task (name='3', parent=t1)
        t3 = Task (name='5', parent=t2)
        
        c1 = Context (name='6')
        c1.add_child(t2_selected)
        
        c2 = Context (name='7')
        c2.add_child(t3)
        
        traverse_list (TaskNameFilterVisitor ('xxx', include=False), [f_on_path])
        
        self.assertTrue(f_on_path.marked)
        self.assertTrue(p_on_path.marked)
        self.assertTrue(t1_on_path.marked)
        self.assertFalse(t2_selected.marked)
        self.assertFalse(t3_on_path.marked)
        
        self.assertTrue(c1.marked)
        self.assertTrue(c2.marked)
        
        self.assertTrue(f.marked)
        self.assertTrue(p.marked)
        self.assertTrue(t1.marked)
        self.assertTrue(t2.marked)
        self.assertTrue(t3.marked)
        self.assertTrue(t4.marked)
        
    def test_Scenario_3 (self):
        '''
        In context mode select a single deeply nested task for inclusion
        '''
        f1 = Folder (name='1')
        p1 = Project (name='2', parent=f1)
        t1 = Task (name='3', parent=p1)
        t2_selected = Task (name='xxx', parent=t1)
        t3 = Task (name='5', parent=t2_selected)
        t4 = Task (name='3', parent=t1)
        
        f2 = Folder (name='1', parent=f1)
        p2 = Project (name='2', parent=f2)
        t5 = Task (name='3', parent=p2)
        t6 = Task (name='3', parent=t5)
        t7 = Task (name='5', parent=t6)
        
        
        c1_on_path = Context (name='6')
        c2_on_path = Context (name='6', parent=c1_on_path)
        c2_on_path.add_child(t2_selected)
        
        c3 = Context (name='7', parent=c2_on_path)
        
        traverse_list (TaskNameFilterVisitor ('xxx'), [c1_on_path], project_mode=False)
        
        self.assertTrue(f1.marked)
        self.assertTrue(p1.marked)
        self.assertTrue(t1.marked)
        self.assertTrue(t2_selected.marked)
        self.assertTrue(t3.marked)
        self.assertTrue(t4.marked)
        self.assertTrue(t5.marked)
        self.assertTrue(t6.marked)
        self.assertTrue(t7.marked)
        self.assertTrue(f2.marked)
        self.assertTrue(p2.marked)
        self.assertTrue(t5.marked)
        self.assertTrue(t6.marked)
        self.assertTrue(t7.marked)
        
        self.assertTrue(c1_on_path.marked)
        self.assertTrue(c2_on_path.marked)
        self.assertFalse(c3.marked)
        
    def test_Scenario_4 (self):
        '''
        In context mode select a single deeply nested task for exclusion
        '''
        f1 = Folder (name='1')
        p1 = Project (name='2', parent=f1)
        t1 = Task (name='3', parent=p1)
        t2_selected = Task (name='xxx', parent=t1)
        t3 = Task (name='5', parent=t2_selected)
        t4 = Task (name='3', parent=t1)
        
        f2 = Folder (name='1', parent=f1)
        p2 = Project (name='2', parent=f2)
        t5 = Task (name='3', parent=p2)
        t6 = Task (name='3', parent=t5)
        t7 = Task (name='5', parent=t6)
        
        
        c1_on_path = Context (name='6')
        c2_on_path = Context (name='6', parent=c1_on_path)
        c2_on_path.add_child(t2_selected)
        
        c3 = Context (name='7', parent=c2_on_path)
        
        traverse_list (TaskNameFilterVisitor ('xxx', include=False), [c1_on_path], project_mode=False)
        
        self.assertTrue(f1.marked)
        self.assertTrue(p1.marked)
        self.assertTrue(t1.marked)
        self.assertFalse(t2_selected.marked)
        self.assertTrue(t3.marked)
        self.assertTrue(t4.marked)
        self.assertTrue(t5.marked)
        self.assertTrue(t6.marked)
        self.assertTrue(t7.marked)
        self.assertTrue(f2.marked)
        self.assertTrue(p2.marked)
        self.assertTrue(t5.marked)
        self.assertTrue(t6.marked)
        self.assertTrue(t7.marked)
        
        self.assertTrue(c1_on_path.marked)
        self.assertTrue(c2_on_path.marked)
        self.assertTrue(c3.marked)