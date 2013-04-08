import re
from datetime import datetime

def format_date_for_matching (now, thedate):
    # be careful - we want whole days, life gets confusing if we want to see
    # todays tasks but we also see some of yesterdays since it's <24hrs ago 
    days_elapsed = (now.date() - thedate.date()).days
    string = thedate.strftime ('%Y-%m-%d %A %B') + ' -' + str (days_elapsed) +'d'
    if days_elapsed == 0:
        string = string + ' today'
    elif days_elapsed == 1:
        string = string + ' yesterday'
    return string

def match_date (now, thedate, range_or_regexp):
    if re.search (' to ', range_or_regexp) != None:
        elements = str.split (range_or_regexp, ' to ')
        elements = [x.strip() for x in elements if len (x) > 0]
        start = datetime.strptime(elements[0], '%Y-%m-%d').date()
        end = datetime.strptime(elements[1], '%Y-%m-%d').date()
        return thedate.date() >= start and thedate.date() <= end
    elif range_or_regexp.startswith ('from'):
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