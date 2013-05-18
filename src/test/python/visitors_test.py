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

import unittest
import re
from treemodel import Folder, Task, Project, Context, traverse_list, traverse, PROJECT, CONTEXT, TASK, FOLDER
from visitors import Filter, Sort

def match_name (item, regexp):
    return re.search (regexp, item.name) != None
    
class Test_visitors(unittest.TestCase):
    
    def test_include (self):
        n1 = Folder (name=u'n1')
        n2 = Folder (name=u'n2 xxx')
        nodes = [n1, n2]
        visitor = Filter ([PROJECT, CONTEXT, TASK, FOLDER], lambda x: match_name(x, 'xxx'), True, "pretty")
        traverse_list (visitor, nodes)
        self.assertFalse(n1.marked)
        self.assertTrue(n2.marked)
    
    def test_exclude (self):
        n1 = Folder (name=u'n1')
        n2 = Folder (name=u'n2 xxx')
        nodes = [n1, n2]
        visitor = Filter ([PROJECT, CONTEXT, TASK, FOLDER], lambda x: match_name(x, 'xxx'), False, 'pretty')
        traverse_list (visitor, nodes)
        self.assertTrue(n1.marked)
        self.assertFalse(n2.marked)
        
    def test__include_ignores_children (self):
        n1 = Folder (name=u'n1 xxx')
        n2 = Folder (name=u'n2')
        n1.add_child(n2)
        
        visitor = Filter ([PROJECT, CONTEXT, TASK, FOLDER], lambda x: match_name(x, 'xxx'), True, 'pretty')
        traverse (visitor, n1)
        self.assertTrue(n1.marked)
        self.assertTrue(n2.marked)
        
    def test_TaskNameFilterVisitor_include (self):
        n1 = Task (name=u'n1')
        n2 = Task (name=u'n2 xxx')
        nodes = [n1, n2]
        visitor = Filter ([PROJECT, CONTEXT, TASK, FOLDER], lambda x: match_name(x, 'xxx'), True, 'pretty')
        traverse_list (visitor, nodes)
        self.assertFalse(n1.marked)
        self.assertTrue(n2.marked)
        
    def test_TaskNameFilterVisitor_exclude (self):
        n1 = Task (name=u'n1')
        n2 = Task (name=u'n2 xxx')
        nodes = [n1, n2]
        visitor = Filter ([PROJECT, CONTEXT, TASK, FOLDER], lambda x: match_name(x, 'xxx'), False, 'pretty')
        traverse_list (visitor, nodes)
        self.assertTrue(n1.marked)
        self.assertFalse(n2.marked)
        
    def test_TaskNameFilterVisitor_include_ignores_children (self):
        n1 = Task (name=u'n1 xxx')
        n2 = Task (name=u'n2')
        n1.add_child(n2)
        
        visitor = Filter ([PROJECT, CONTEXT, TASK, FOLDER], lambda x: match_name(x, 'xxx'), True, 'pretty')
        traverse (visitor, n1)
        self.assertTrue(n1.marked)
        self.assertTrue(n2.marked)
    
    def test_Sort_in_order (self):
        n1 = Task (name=u'a n1')
        n2 = Task (name=u'b n2')
        root = Project (name=u'r')
        root.add_child(n1)
        root.add_child(n2)
        
        visitor = Sort ([PROJECT], lambda x: x.name, 'pretty')
        traverse (visitor, root)
        self.assertIs(root.children[0], n1)
        self.assertIs(root.children[1], n2)
        
    def test_Sort_out_of__order (self):
        n1 = Task (name=u'b n1')
        n2 = Task (name=u'a n2')
        root = Project (name=u'r')
        root.add_child(n1)
        root.add_child(n2)
        
        visitor = Sort ([PROJECT], lambda x: x.name, 'pretty')
        traverse (visitor, root)
        self.assertIs(root.children[0], n2)
        self.assertIs(root.children[1], n1)
        
    def test_Sort_same_use_underlying_order_in_order (self):
        n1 = Task (name=u'aaa', order=1)
        n2 = Task (name=u'aaa', order=2)
        root = Project (name=u'r')
        root.add_child(n1)
        root.add_child(n2)
        
        visitor = Sort ([PROJECT], lambda x: x.name, 'pretty')
        traverse (visitor, root)
        self.assertIs(root.children[0], n1)
        self.assertIs(root.children[1], n2)
        
    def test_Sort_same_use_underlying_order_out_of_order (self):
        n1 = Task (name=u'aaa', order=2)
        n2 = Task (name=u'aaa', order=1)
        root = Project (name=u'r')
        root.add_child(n1)
        root.add_child(n2)
        
        visitor = Sort ([PROJECT], lambda x: x.name, 'pretty')
        traverse (visitor, root)
        self.assertIs(root.children[0], n2)
        self.assertIs(root.children[1], n1)
    
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
        
        traverse_list (Filter ([PROJECT, CONTEXT, TASK, FOLDER], lambda x: match_name(x, 'xxx'), True, 'pretty'), [f_on_path])
        
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
        
        traverse_list (Filter ([PROJECT, CONTEXT, TASK, FOLDER], lambda x: match_name(x, 'xxx'), False, 'pretty'), [f_on_path])
        
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
        
        traverse_list (Filter ([PROJECT, CONTEXT, TASK, FOLDER], lambda x: match_name(x, 'xxx'), True, 'pretty'), [c1_on_path], project_mode=False)
        
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
        
        traverse_list (Filter ([PROJECT, CONTEXT, TASK, FOLDER], lambda x: match_name(x, 'xxx'), False, 'pretty'), [c1_on_path], project_mode=False)
        
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