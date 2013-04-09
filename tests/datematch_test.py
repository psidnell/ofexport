import unittest
from datematch import format_date_for_matching, match_date, date_from_string
from datetime import datetime

class Test_datematch(unittest.TestCase):
    
    def test_date_from_string (self):
        tue = datetime.strptime('Apr 9 2013  11:33PM', '%b %d %Y %I:%M%p')
        
        self.assertEquals("2013-04-08", date_from_string (tue,"monday").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-09", date_from_string (tue,"tues").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-10", date_from_string (tue,"wed").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-11", date_from_string (tue,"th").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-12", date_from_string (tue,"fr").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-13", date_from_string (tue,"sa").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-14", date_from_string (tue,"su").strftime ("%Y-%m-%d"))
        
        self.assertEquals("2013-04-09", date_from_string (tue,"today").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-08", date_from_string (tue,"yesterday").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-10", date_from_string (tue,"tomorrow").strftime ("%Y-%m-%d"))

        self.assertEquals("2013-04-15", date_from_string (tue,"next monday").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-16", date_from_string (tue,"next tuesday").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-17", date_from_string (tue,"next wednesday").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-18", date_from_string (tue,"next thurs").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-19", date_from_string (tue,"next fr").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-20", date_from_string (tue,"next sa").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-21", date_from_string (tue,"next su").strftime ("%Y-%m-%d"))
        try:
            self.assertEquals("2013-04-14", date_from_string (tue,"next monkey").strftime ("%Y-%m-%d"))
            self.fail('Exception expected')
        except Exception as e:
            self.assertEquals ('I don\'t think "monkey" is a real day', e.message)
        self.assertEquals("2013-04-01", date_from_string (tue,"last mo").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-02", date_from_string (tue,"last tu").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-03", date_from_string (tue,"last we").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-04", date_from_string (tue,"last th").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-05", date_from_string (tue,"last fr").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-06", date_from_string (tue,"last sa").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-07", date_from_string (tue,"last su").strftime ("%Y-%m-%d"))
        
        try:
            self.assertEquals("2013-04-14", date_from_string (tue,"last monkey").strftime ("%Y-%m-%d"))
            self.fail('Exception expected')
        except Exception as e:
            self.assertEquals ('I don\'t think "monkey" is a real day', e.message)
        self.assertEquals("2013-04-08", date_from_string (tue,"mo").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-09", date_from_string (tue,"tu").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-10", date_from_string (tue,"we").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-11", date_from_string (tue,"th").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-12", date_from_string (tue,"fri").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-13", date_from_string (tue,"sat").strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-14", date_from_string (tue,"sun").strftime ("%Y-%m-%d"))
            
    def test_date_formatting (self):
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 5 2005  11:33PM', '%b %d %Y %I:%M%p')
        string = format_date_for_matching (now, completion)
        self.assertEquals("2005-06-01 wednesday june -4d", string)
        
    def test_date_formatting_today (self):
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 1 2005  11:33PM', '%b %d %Y %I:%M%p')
        string = format_date_for_matching (now, completion)
        self.assertEquals("2005-06-01 wednesday june -0d today", string)
        
    def test_date_formatting_yesterday (self):
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        now = datetime.strptime('Jun 2 2005  11:33PM', '%b %d %Y %I:%M%p')
        string = format_date_for_matching (now, completion)
        self.assertEquals("2005-06-01 wednesday june -1d yesterday", string)
        
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
        sun = datetime.strptime('Apr 7 2013  1:33AM', '%b %d %Y %I:%M%p')
        now_mon = datetime.strptime('Apr 8 2013  1:33AM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (now_mon, sun, "Last Sunday"))
        
        # no match
        sat = datetime.strptime('Apr 6 2013  1:33AM', '%b %d %Y %I:%M%p')
        now_mon = datetime.strptime('Apr 8 2013  1:33AM', '%b %d %Y %I:%M%p')
        self.assertFalse(match_date (now_mon, sat, "Last Sun"))
        
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

    def test_match_date_from_date (self):
        
        # before
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        self.assertFalse(match_date (None, completion, "from 2005-06-02"))
        
        # after
        completion = datetime.strptime('Jun 3 2005  1:33AM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (None, completion, "from 2005-06-02"))
        
        # on
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (None, completion, "from 2005-06-01"))
        
    def test_match_date_to_date (self):
        
        # before
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (None, completion, "to 2005-06-02"))
        
        # after
        completion = datetime.strptime('Jun 3 2005  1:33AM', '%b %d %Y %I:%M%p')
        self.assertFalse(match_date (None, completion, "to 2005-06-02"))
        
        # on
        completion = datetime.strptime('Jun 1 2005  1:33AM', '%b %d %Y %I:%M%p')
        self.assertTrue(match_date (None, completion, "from 2005-06-01"))
        
    def test_match_date_from_day (self):
        mon = datetime.strptime('Apr 8 2013  1:33AM', '%b %d %Y %I:%M%p')
        tue = datetime.strptime('Apr 9 2013  1:33AM', '%b %d %Y %I:%M%p')
        wed = datetime.strptime('Apr 10 2013  1:33AM', '%b %d %Y %I:%M%p')
        
        # before
        now_wed = wed
        self.assertFalse(match_date (now_wed, mon, "from tuesday"))
        
        # after
        completion = tue
        now = wed
        self.assertTrue(match_date (now, completion, "from Monday"))
        self.assertTrue(match_date (now, completion, "from Tue"))
        
        # on
        completion = tue
        now = wed
        self.assertTrue(match_date (now, completion, "from Tuesday"))
        self.assertTrue(match_date (now, completion, "from Tue"))
        
    def test_match_date_this_week (self):
        sat = datetime.strptime('Apr 7 2013  1:33AM', '%b %d %Y %I:%M%p')
        mon = datetime.strptime('Apr 8 2013  1:33AM', '%b %d %Y %I:%M%p')
        tue = datetime.strptime('Apr 9 2013  1:33AM', '%b %d %Y %I:%M%p')
        wed = datetime.strptime('Apr 10 2013  1:33AM', '%b %d %Y %I:%M%p')
        
        # before
        completion = sat
        now = wed
        self.assertFalse(match_date (now, completion, "this week"))
        
        # after
        completion = tue
        now = wed
        self.assertTrue(match_date (now, completion, "this week"))
        
        # on
        completion = mon
        now = wed
        self.assertTrue(match_date (now, completion, "this week"))


