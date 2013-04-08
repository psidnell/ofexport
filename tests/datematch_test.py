import unittest
from datematch import format_date_for_matching, match_date
from datetime import datetime

class Test_datematch(unittest.TestCase):
    
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

