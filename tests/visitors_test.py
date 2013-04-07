import unittest
from visitors import FolderNameFilterVisitor
from treemodel import Folder, traverse_list
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
