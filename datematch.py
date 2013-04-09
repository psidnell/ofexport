import re
from datetime import datetime, timedelta

def hunt_for_day (now, dow, forward, match_today = False):
    direction = -1
    start = 1
    if forward:
        direction = 1
    if match_today:
        start = 0
    for days in range (start, 8):
        next_date = now + timedelta(days=days*direction)
        next_dow = next_date.strftime ('%A').lower()
        if next_dow.startswith (dow):
            return next_date
    raise Exception ('I don\'t think "' + dow + '" is a real day')

def find_monday_this_week (now):
    return hunt_for_day (now, 'mo', False, match_today=True)

def find_monday_next_week (now):
    return hunt_for_day (now, 'mo', True, match_today=False)

def date_from_string (now, date_str):
    if date_str == "today":
        return now
    elif date_str == 'yesterday':
        return now + timedelta(days=-1)
    elif date_str == 'tomorrow':
        return now + timedelta(days=1)
    elif re.match ('^next [mtwfs][aouehr]', date_str) != None:
        dow = date_str[4:].strip ()
        next_monday = find_monday_next_week (now)
        return hunt_for_day (next_monday, dow, True, match_today=True)
    elif re.match ('^last [mtwfs][aouehr]', date_str) != None:
        dow = date_str[4:].strip ()
        this_monday = find_monday_this_week (now)
        return hunt_for_day (this_monday, dow, False)
    elif re.match ('^[mtwfs][aouehr]', date_str) != None:
        dow = date_str.strip ()
        monday = find_monday_this_week (now)
        return hunt_for_day (monday, dow, True, match_today=True)
    elif re.match ('^[0-9][0-9][0-9][0-9]-[01][0-9]-[0-3][0-9]$', date_str) != None:
        return datetime.strptime(date_str, '%Y-%m-%d')
    else:
        raise Exception ('I don\'t think "' + date_str + '" is any kind of date specification I recognise')

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
    
    if thedate == None:
        return range_or_regexp.strip() == ''
    
    try:
        match_date = date_from_string (now, range_or_regexp)
        return thedate.date() == match_date.date()
    except:
        pass
    
    if range_or_regexp == 'this week':
        mon = find_monday_this_week (now)
        sun = hunt_for_day (now, 'sun', True, match_today=True)
        return thedate.date() >= mon.date() and thedate.date() <= sun.date()
    elif range_or_regexp == 'next week':
        mon = find_monday_this_week (now) + timedelta(days=7)
        sun = hunt_for_day (now, 'sun', True, match_today=True) + timedelta(days=7)
        return thedate.date() >= mon.date() and thedate.date() <= sun.date()
    elif range_or_regexp == 'last week':
        mon = find_monday_this_week (now) - timedelta(days=7)
        sun = hunt_for_day (now, 'sun', True, match_today=True) - timedelta(days=7)
        return thedate.date() >= mon.date() and thedate.date() <= sun.date()
    elif range_or_regexp.startswith ('from '):
        date_str = range_or_regexp[4:].strip()
        start =  date_from_string (now, date_str)
        return thedate.date() >= start.date()
    elif range_or_regexp.startswith ('to '):
        date_str = range_or_regexp[2:].strip()
        end =  date_from_string (now, date_str)
        return thedate.date() <= end.date()
    elif re.search (' to ', range_or_regexp) != None:
        if thedate == None:
            return False
        elements = str.split (range_or_regexp, ' to ')
        elements = [x.strip() for x in elements if len (x) > 0]
        start = datetime.strptime(elements[0], '%Y-%m-%d').date()
        end = datetime.strptime(elements[1], '%Y-%m-%d').date()
        return thedate.date() >= start and thedate.date() <= end
    else:
        return re.search(range_or_regexp, format_date_for_matching (now, thedate)) != None