import re
from datetime import datetime, timedelta

'''
    Specific matching formats:
        date range: 2013-03-28 to 2013-04-08
        everything since a specific date: from 2013-03-28
        from DOW: from Mon, from Monday
        this week (since Monday): this week
    Anything else is considered a regular expression but the date it's matching on
    is designed to make things easy: eg
        2013-04-06 April Saturday -0d today
        2013-04-05 April Friday -1d yesterday
        2013-04-04 April Thursday -0d today
    So without resorting to fancy matching you can search for:
        specific date: 2013-04-08
        today: today
        yesterday: yesterday
    Or getting fancier:
        the last week: -[0-7]d
        any Monday: Monday
'''
def format_date_for_matching (now, thedate):
    # be careful - we want whole days, life gets confusing if we want to see
    # todays tasks but we also see some of yesterdays since it's <24hrs ago 
    days_elapsed = (now.date() - thedate.date()).days
    string = thedate.strftime ('%Y-%m-%d %A %B') + ' -' + str (days_elapsed) +'d'
    if days_elapsed == 0:
        string = string + ' today'
    elif days_elapsed == 1:
        string = string + ' yesterday'
    return string.lower()

def match_date (now, thedate, range_or_regexp):
    range_or_regexp = range_or_regexp.lower ()
    
    if range_or_regexp.startswith ('this week'):
        range_or_regexp = 'from mon'
        
    if re.search ('from [mon|tue|wed|thu|fri]', range_or_regexp) != None:
        if thedate == None:
            return False
        elements = str.split (range_or_regexp)
        elements = [x.strip() for x in elements if len (x) > 0]
        day = elements[1]
        start = None
        for ago in range(0, 6):
            if start == None: # YUK - find out how to break out of the loop
                poss_date = now - timedelta(days=ago)
                if poss_date.strftime('%A').lower().startswith (day):
                    start = poss_date.date()
        return thedate.date() >= start
    elif re.search (' to ', range_or_regexp) != None:
        if thedate == None:
            return False
        elements = str.split (range_or_regexp, ' to ')
        elements = [x.strip() for x in elements if len (x) > 0]
        start = datetime.strptime(elements[0], '%Y-%m-%d').date()
        end = datetime.strptime(elements[1], '%Y-%m-%d').date()
        return thedate.date() >= start and thedate.date() <= end
    elif range_or_regexp.startswith ('from'):
        if thedate == None:
            return False
        elements = str.split (range_or_regexp, 'from')
        elements = [x.strip() for x in elements if len (x) > 0]
        start = datetime.strptime(elements[0], '%Y-%m-%d').date()
        return thedate.date() >= start
    else:
        if thedate != None:
            date_str = format_date_for_matching (now, thedate)
        else:
            date_str = ''
        return re.search (range_or_regexp, date_str) != None