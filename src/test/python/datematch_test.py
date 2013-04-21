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
from datematch import date_range_to_str, tidy_space_separated_fields, process_date_specifier, hunt_for_day, find_first_of_month, find_next_month, find_prev_month, find_end_of_month, find_january_this_year, hunt_for_month, find_monday_this_week, find_monday_next_week
from datetime import datetime

def process_date_specifier_to_datestr (now, spec):
        rng = process_date_specifier (now, spec)
        return date_range_to_str (rng)
    
class Test_datematch(unittest.TestCase):
    
    def test_tidy_space_separated_fields(self):
        self.assertEquals ("a bb ccc dddd", tidy_space_separated_fields (" a   bb ccc   dddd  "))
    
    def test_hunt_for_day (self):
        tue = datetime.strptime('Apr 9 2013 11:33PM', '%b %d %Y %I:%M%p')
        
        self.assertEquals("2013-04-15", hunt_for_day (tue,"monday", True, match_today = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-09", hunt_for_day (tue,"tue", True, match_today = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-10", hunt_for_day (tue,"we", True, match_today = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-11", hunt_for_day (tue,"th", True, match_today = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-12", hunt_for_day (tue,"fr", True, match_today = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-13", hunt_for_day (tue,"sa", True, match_today = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-14", hunt_for_day (tue,"su", True, match_today = True).date().strftime ("%Y-%m-%d"))
        
        self.assertEquals("2013-04-15", hunt_for_day (tue,"monday", True, match_today = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-16", hunt_for_day (tue,"tue", True, match_today = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-10", hunt_for_day (tue,"we", True, match_today = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-11", hunt_for_day (tue,"th", True, match_today = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-12", hunt_for_day (tue,"fr", True, match_today = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-13", hunt_for_day (tue,"sa", True, match_today = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-14", hunt_for_day (tue,"su", True, match_today = False).date().strftime ("%Y-%m-%d"))
        
        self.assertEquals("2013-04-08", hunt_for_day (tue,"monday", False, match_today = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-09", hunt_for_day (tue,"tue", False, match_today = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-03", hunt_for_day (tue,"we", False, match_today = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-04", hunt_for_day (tue,"th", False, match_today = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-05", hunt_for_day (tue,"fr", False, match_today = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-06", hunt_for_day (tue,"sa", False, match_today = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-07", hunt_for_day (tue,"su", False, match_today = True).date().strftime ("%Y-%m-%d"))
        
        self.assertEquals("2013-04-08", hunt_for_day (tue,"monday", False, match_today = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-02", hunt_for_day (tue,"tue", False, match_today = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-03", hunt_for_day (tue,"we", False, match_today = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-04", hunt_for_day (tue,"th", False, match_today = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-05", hunt_for_day (tue,"fr", False, match_today = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-06", hunt_for_day (tue,"sa", False, match_today = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-07", hunt_for_day (tue,"su", False, match_today = False).date().strftime ("%Y-%m-%d"))
    
    def test_find_monday_this_week (self):
        mon = datetime.strptime('Apr 8 2013 11:33PM', '%b %d %Y %I:%M%p')
        sun = datetime.strptime('Apr 14 2013 11:33PM', '%b %d %Y %I:%M%p')
        
        self.assertEquals("2013-04-08", find_monday_this_week (mon).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-08", find_monday_this_week (sun).date().strftime ("%Y-%m-%d"))
        
    def test_find_monday_next_week (self):
        mon = datetime.strptime('Apr 8 2013 11:33PM', '%b %d %Y %I:%M%p')
        sun = datetime.strptime('Apr 14 2013 11:33PM', '%b %d %Y %I:%M%p')
        
        self.assertEquals("2013-04-15", find_monday_next_week (mon).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-15", find_monday_next_week (sun).date().strftime ("%Y-%m-%d"))
    
    def test_find_first_of_month (self):
        first = datetime.strptime('Apr 1 2013 11:33PM', '%b %d %Y %I:%M%p')
        last = datetime.strptime('Apr 30 2013 11:33PM', '%b %d %Y %I:%M%p')
        
        self.assertEquals("2013-04-01", find_first_of_month (first).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-01", find_first_of_month (last).date().strftime ("%Y-%m-%d"))
        
    def test_find_january_this_year (self):
        first = datetime.strptime('Jan 1 2013 11:33PM', '%b %d %Y %I:%M%p')
        last = datetime.strptime('Dec 30 2013 11:33PM', '%b %d %Y %I:%M%p')
        
        self.assertEquals("2013-01-01", find_january_this_year (first).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-01-01", find_january_this_year (last).date().strftime ("%Y-%m-%d"))
        
    def test_find_next_month (self):
        first = datetime.strptime('Apr 1 2013 11:33PM', '%b %d %Y %I:%M%p')
        last = datetime.strptime('Apr 30 2013 11:33PM', '%b %d %Y %I:%M%p')
        
        self.assertEquals("2013-05-01", find_next_month (first).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-05-01", find_next_month (last).date().strftime ("%Y-%m-%d"))
        
    def test_find_prev_month (self):
        first = datetime.strptime('Apr 1 2013 11:33PM', '%b %d %Y %I:%M%p')
        last = datetime.strptime('Apr 30 2013 11:33PM', '%b %d %Y %I:%M%p')
        
        self.assertEquals("2013-03-01", find_prev_month (first).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-03-01", find_prev_month (last).date().strftime ("%Y-%m-%d"))
        
    def test_find_end_of_month (self):
        first = datetime.strptime('Apr 1 2013 11:33PM', '%b %d %Y %I:%M%p')
        last = datetime.strptime('Apr 30 2013 11:33PM', '%b %d %Y %I:%M%p')
        
        self.assertEquals("2013-04-30", find_end_of_month (first).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-30", find_end_of_month (last).date().strftime ("%Y-%m-%d"))
    
    def test_hunt_for_month (self):
        apr = datetime.strptime('Apr 9 2013 11:33PM', '%b %d %Y %I:%M%p')
        
        self.assertEquals("2014-01-01", hunt_for_month (apr,"january", True, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2014-02-01", hunt_for_month (apr,"feb", True, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2014-03-01", hunt_for_month (apr,"mar", True, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-01", hunt_for_month (apr,"apr", True, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-05-01", hunt_for_month (apr,"may", True, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-06-01", hunt_for_month (apr,"jun", True, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-07-01", hunt_for_month (apr,"jul", True, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-08-01", hunt_for_month (apr,"aug", True, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-09-01", hunt_for_month (apr,"sep", True, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-10-01", hunt_for_month (apr,"oct", True, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-11-01", hunt_for_month (apr,"nov", True, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-12-01", hunt_for_month (apr,"dec", True, match_this_month = True).date().strftime ("%Y-%m-%d"))
        
        self.assertEquals("2014-01-01", hunt_for_month (apr,"january", True, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2014-02-01", hunt_for_month (apr,"feb", True, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2014-03-01", hunt_for_month (apr,"mar", True, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2014-04-01", hunt_for_month (apr,"apr", True, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-05-01", hunt_for_month (apr,"may", True, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-06-01", hunt_for_month (apr,"jun", True, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-07-01", hunt_for_month (apr,"jul", True, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-08-01", hunt_for_month (apr,"aug", True, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-09-01", hunt_for_month (apr,"sep", True, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-10-01", hunt_for_month (apr,"oct", True, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-11-01", hunt_for_month (apr,"nov", True, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-12-01", hunt_for_month (apr,"dec", True, match_this_month = False).date().strftime ("%Y-%m-%d"))
        
        self.assertEquals("2013-01-01", hunt_for_month (apr,"january", False, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-02-01", hunt_for_month (apr,"feb", False, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-03-01", hunt_for_month (apr,"mar", False, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-04-01", hunt_for_month (apr,"apr", False, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-05-01", hunt_for_month (apr,"may", False, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-06-01", hunt_for_month (apr,"jun", False, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-07-01", hunt_for_month (apr,"jul", False, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-08-01", hunt_for_month (apr,"aug", False, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-09-01", hunt_for_month (apr,"sep", False, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-10-01", hunt_for_month (apr,"oct", False, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-11-01", hunt_for_month (apr,"nov", False, match_this_month = True).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-12-01", hunt_for_month (apr,"dec", False, match_this_month = True).date().strftime ("%Y-%m-%d"))
        
        self.assertEquals("2013-01-01", hunt_for_month (apr,"january", False, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-02-01", hunt_for_month (apr,"feb", False, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2013-03-01", hunt_for_month (apr,"mar", False, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-04-01", hunt_for_month (apr,"apr", False, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-05-01", hunt_for_month (apr,"may", False, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-06-01", hunt_for_month (apr,"jun", False, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-07-01", hunt_for_month (apr,"jul", False, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-08-01", hunt_for_month (apr,"aug", False, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-09-01", hunt_for_month (apr,"sep", False, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-10-01", hunt_for_month (apr,"oct", False, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-11-01", hunt_for_month (apr,"nov", False, match_this_month = False).date().strftime ("%Y-%m-%d"))
        self.assertEquals("2012-12-01", hunt_for_month (apr,"dec", False, match_this_month = False).date().strftime ("%Y-%m-%d"))
    
    def test_date_from_string (self):
        tue = datetime.strptime('Apr 9 2013 11:33PM', '%b %d %Y %I:%M%p')
                
        self.assertEquals("2013-04-08", process_date_specifier_to_datestr (tue,"monday"))
        self.assertEquals("2013-04-09", process_date_specifier_to_datestr (tue,"tues"))
        self.assertEquals("2013-04-10", process_date_specifier_to_datestr (tue,"wed"))
        self.assertEquals("2013-04-11", process_date_specifier_to_datestr (tue,"th"))
        self.assertEquals("2013-04-12", process_date_specifier_to_datestr (tue,"fr"))
        self.assertEquals("2013-04-13", process_date_specifier_to_datestr (tue,"sa"))
        self.assertEquals("2013-04-14", process_date_specifier_to_datestr (tue,"su"))

        self.assertEquals("2013-04-15", process_date_specifier_to_datestr (tue,"next monday"))
        self.assertEquals("2013-04-16", process_date_specifier_to_datestr (tue,"next tuesday"))
        self.assertEquals("2013-04-17", process_date_specifier_to_datestr (tue,"next wednesday"))
        self.assertEquals("2013-04-18", process_date_specifier_to_datestr (tue,"next thurs"))
        self.assertEquals("2013-04-19", process_date_specifier_to_datestr (tue,"next fr"))
        self.assertEquals("2013-04-20", process_date_specifier_to_datestr (tue,"next sa"))
        self.assertEquals("2013-04-21", process_date_specifier_to_datestr (tue,"next su"))
        try:
            self.assertEquals("2013-04-14", process_date_specifier_to_datestr (tue,"next monkey"))
            self.fail('Exception expected')
        except Exception as e:
            self.assertEquals ('I don\'t think "next monkey" is any kind of date specification I recognise', e.message)
        self.assertEquals("2013-04-01", process_date_specifier_to_datestr (tue,"last mo"))
        self.assertEquals("2013-04-02", process_date_specifier_to_datestr (tue,"last tu"))
        self.assertEquals("2013-04-03", process_date_specifier_to_datestr (tue,"last we"))
        self.assertEquals("2013-04-04", process_date_specifier_to_datestr (tue,"last th"))
        self.assertEquals("2013-04-05", process_date_specifier_to_datestr (tue,"last fr"))
        self.assertEquals("2013-04-06", process_date_specifier_to_datestr (tue,"last sa"))
        self.assertEquals("2013-04-07", process_date_specifier_to_datestr (tue,"last su"))
        
        try:
            self.assertEquals("2013-04-14", process_date_specifier_to_datestr (tue,"last monkey"))
            self.fail('Exception expected')
        except Exception as e:
            self.assertEquals ('I don\'t think "last monkey" is any kind of date specification I recognise', e.message)
        self.assertEquals("2013-04-08", process_date_specifier_to_datestr (tue,"mo"))
        self.assertEquals("2013-04-09", process_date_specifier_to_datestr (tue,"tu"))
        self.assertEquals("2013-04-10", process_date_specifier_to_datestr (tue,"we"))
        self.assertEquals("2013-04-11", process_date_specifier_to_datestr (tue,"th"))
        self.assertEquals("2013-04-12", process_date_specifier_to_datestr (tue,"fri"))
        self.assertEquals("2013-04-13", process_date_specifier_to_datestr (tue,"sat"))
        self.assertEquals("2013-04-14", process_date_specifier_to_datestr (tue,"sun"))
        
        self.assertEquals("2013-01-01..2013-01-31", process_date_specifier_to_datestr (tue,"january"))
        self.assertEquals("2013-02-01..2013-02-28", process_date_specifier_to_datestr (tue,"feb"))
        self.assertEquals("2013-03-01..2013-03-31", process_date_specifier_to_datestr (tue,"mar"))
        self.assertEquals("2013-04-01..2013-04-30", process_date_specifier_to_datestr (tue,"apr"))
        self.assertEquals("2013-05-01..2013-05-31", process_date_specifier_to_datestr (tue,"may"))
        self.assertEquals("2013-06-01..2013-06-30", process_date_specifier_to_datestr (tue,"jun"))
        self.assertEquals("2013-07-01..2013-07-31", process_date_specifier_to_datestr (tue,"jul"))
        self.assertEquals("2013-08-01..2013-08-31", process_date_specifier_to_datestr (tue,"aug"))
        self.assertEquals("2013-09-01..2013-09-30", process_date_specifier_to_datestr (tue,"sep"))
        self.assertEquals("2013-10-01..2013-10-31", process_date_specifier_to_datestr (tue,"oct"))
        self.assertEquals("2013-11-01..2013-11-30", process_date_specifier_to_datestr (tue,"nov"))
        self.assertEquals("2013-12-01..2013-12-31", process_date_specifier_to_datestr (tue,"dec"))
        
        self.assertEquals("2014-01-01..2014-01-31", process_date_specifier_to_datestr (tue,"next january"))
        self.assertEquals("2014-02-01..2014-02-28", process_date_specifier_to_datestr (tue,"next feb"))
        self.assertEquals("2014-03-01..2014-03-31", process_date_specifier_to_datestr (tue,"next mar"))
        self.assertEquals("2014-04-01..2014-04-30", process_date_specifier_to_datestr (tue,"next apr"))
        self.assertEquals("2014-05-01..2014-05-31", process_date_specifier_to_datestr (tue,"next may"))
        self.assertEquals("2014-06-01..2014-06-30", process_date_specifier_to_datestr (tue,"next jun"))
        self.assertEquals("2014-07-01..2014-07-31", process_date_specifier_to_datestr (tue,"next jul"))
        self.assertEquals("2014-08-01..2014-08-31", process_date_specifier_to_datestr (tue,"next aug"))
        self.assertEquals("2014-09-01..2014-09-30", process_date_specifier_to_datestr (tue,"next sep"))
        self.assertEquals("2014-10-01..2014-10-31", process_date_specifier_to_datestr (tue,"next oct"))
        self.assertEquals("2014-11-01..2014-11-30", process_date_specifier_to_datestr (tue,"next nov"))
        self.assertEquals("2014-12-01..2014-12-31", process_date_specifier_to_datestr (tue,"next dec"))
        
        self.assertEquals("2012-01-01..2012-01-31", process_date_specifier_to_datestr (tue,"last january"))
        self.assertEquals("2012-02-01..2012-02-29", process_date_specifier_to_datestr (tue,"last feb"))
        self.assertEquals("2012-03-01..2012-03-31", process_date_specifier_to_datestr (tue,"last mar"))
        self.assertEquals("2012-04-01..2012-04-30", process_date_specifier_to_datestr (tue,"last apr"))
        self.assertEquals("2012-05-01..2012-05-31", process_date_specifier_to_datestr (tue,"last may"))
        self.assertEquals("2012-06-01..2012-06-30", process_date_specifier_to_datestr (tue,"last jun"))
        self.assertEquals("2012-07-01..2012-07-31", process_date_specifier_to_datestr (tue,"last jul"))
        self.assertEquals("2012-08-01..2012-08-31", process_date_specifier_to_datestr (tue,"last aug"))
        self.assertEquals("2012-09-01..2012-09-30", process_date_specifier_to_datestr (tue,"last sep"))
        self.assertEquals("2012-10-01..2012-10-31", process_date_specifier_to_datestr (tue,"last oct"))
        self.assertEquals("2012-11-01..2012-11-30", process_date_specifier_to_datestr (tue,"last nov"))
        self.assertEquals("2012-12-01..2012-12-31", process_date_specifier_to_datestr (tue,"last dec"))
        
        self.assertEquals("any", process_date_specifier_to_datestr (tue,"any"))
        self.assertEquals("none", process_date_specifier_to_datestr (tue,"none"))
        self.assertEquals("none", process_date_specifier_to_datestr (tue, ''))
        
        self.assertEquals("2013-04-09", process_date_specifier_to_datestr (tue,"today"))
        self.assertEquals("2013-04-08", process_date_specifier_to_datestr (tue,"yesterday"))
        self.assertEquals("2013-04-10", process_date_specifier_to_datestr (tue,"tomorrow"))
        
        self.assertEquals("2013-04-07..", process_date_specifier_to_datestr (tue,"from last sun"))
        self.assertEquals("2013-02-01..", process_date_specifier_to_datestr (tue,"from feb"))
        self.assertEquals("2012-02-01..", process_date_specifier_to_datestr (tue,"from last feb"))
        
        self.assertEquals("..2013-04-10", process_date_specifier_to_datestr (tue,"to tomorrow"))
        self.assertEquals("..2013-08-31", process_date_specifier_to_datestr (tue,"to aug"))
        self.assertEquals("..2014-08-31", process_date_specifier_to_datestr (tue,"to next aug"))
        
        self.assertEquals("2013-04-07..2013-04-10", process_date_specifier_to_datestr (tue,"last sun to tomorrow"))
        self.assertEquals("2013-04-08..2013-04-09", process_date_specifier_to_datestr (tue,"yesterday to today"))
        self.assertEquals("2013-04-09..2013-04-15", process_date_specifier_to_datestr (tue,"today to next mon"))
        self.assertEquals("2012-01-01..2014-12-31", process_date_specifier_to_datestr (tue,"last jan to next dec"))
        self.assertEquals("2012-01-01..2014-12-31", process_date_specifier_to_datestr (tue,"2012-01-01 to 2014-12-31"))

        
