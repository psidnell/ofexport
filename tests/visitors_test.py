import unittest
from visitors import FolderNameFilterVisitor, TaskNameFilterVisitor, ProjectNameFilterVisitor, ContextNameFilterVisitor, format_date_for_matching, match_date
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
        
    def test_date_formatting (self):
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 5 2005  11:33PM', '%b %d %Y %I:%M%p')
        string = format_date_for_matching (now, completion)
        self.assertEquals("2005-06-01 Wednesday June -4d", string)
        
    def test_date_formatting_today (self):
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 1 2005  11:33PM', '%b %d %Y %I:%M%p')
        string = format_date_for_matching (now, completion)
        self.assertEquals("2005-06-01 Wednesday June -0d today", string)
        
    def test_date_formatting_yesterday (self):
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')
        string = format_date_for_matching (now, completion)
        self.assertEquals("2005-06-01 Wednesday June -1d yesterday", string)
        
    def test_match_date_specific_date (self):
        
        # match
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (now, completion, "2005-06-01"))
        
        # no match
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')
        self.assertFalse(match_date (now, completion, "2005-06-02"))
        
    def test_match_date_month (self):
        
        # match
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (now, completion, "June"))
        
        # no match
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')
        self.assertFalse(match_date (now, completion, "July"))
    
    def test_match_date_day (self):
        
        # match
        completion = datetime.strptime('Apr 8 2013  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (now, completion, "Monday"))
        
        # no match
        completion = datetime.strptime('Apr 8 2013  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')
        self.assertFalse(match_date (now, completion, "Tuesday"))
        
    def test_match_date_today (self):
        
        # match
        completion = datetime.strptime('Apr 8 2013  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Apr 8 2013  1:33AM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (now, completion, "today"))
        
        # no match
        completion = datetime.strptime('Apr 7 2013  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Apr 8 2013  1:33AM', '%b %d %Y %I:%M%p')
        self.assertFalse(match_date (now, completion, "today"))
        
    def test_match_date_yesterday (self):
        
        # match
        completion = datetime.strptime('Apr 7 2013  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Apr 8 2013  1:33AM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (now, completion, "yesterday"))
        
        # no match
        completion = datetime.strptime('Apr 8 2013  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Apr 8 2013  1:33AM', '%b %d %Y %I:%M%p')
        self.assertFalse(match_date (now, completion, "yesterday"))
        
    def test_match_date_range (self):
        
        # within
        completion = datetime.strptime('Jun 5 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')   
        self.assertTrue(match_date (now, completion, "2005-06-01 to 2005-06-10"))
        
        # before
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')  
        self.assertFalse(match_date (now, completion, "2005-06-02 to 2005-06-10"))
        
        # after
        completion = datetime.strptime('Jun 11 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')   
        self.assertFalse(match_date (now, completion, "2005-06-02 to 2005-06-10"))
        
        # on start
        completion = datetime.strptime('Jun 6 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (now, completion, "2005-06-01 to 2005-06-10"))
        
        # on end
        completion = datetime.strptime('Jun 10 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (now, completion, "2005-06-01 to 2005-06-10"))


    def test_match_date_from (self):
        
        # before
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        self.assertFalse(match_date (None, completion, "from 2005-06-02"))
        
        # after
        completion = datetime.strptime('Jun 3 2005  1:33AM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (None, completion, "from 2005-06-02"))
        
        # on
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (None, completion, "from 2005-06-01"))

