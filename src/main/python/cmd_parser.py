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

import re
from treemodel import TASK, PROJECT, CONTEXT, FOLDER, Note
from datetime import datetime
from datematch import process_date_specifier, match_date_against_range, date_range_to_str
from visitors import Filter, Prune, Sort, Flatten
import logging

LOGGER = logging.getLogger(__name__)

the_time = None
NOW = datetime.now()
FAR_FUTURE = datetime.strptime("3000-01-01", "%Y-%m-%d")

def now ():
    # allows us to test with a fixed date
    if the_time != None:
        return the_time
    return NOW

# Primary/Real name is first
NAME_ALIASES = ['name', 'title', 'text', 'name']
START_ALIASES = ['date_to_start', 'start', 'started', 'begin', 'began']
COMPLETED_ALIASES = ['date_completed', 'done', 'end', 'ended', 'complete', 'completed', 'finish', 'finished', 'completion']
DUE_ALIASES = ['date_due', 'due', 'deadline']
FLAGGED_ALIASES = ['flagged', 'flag']
NEXT_ALIASES = ['next', 'next']
TYPE_ALIASES = ['type']
NOTE_ALIASES = ['note']
STATUS_ALIASES = ['status']

FLATTEN_ALIASES = ['flat', 'flatten']
PRUNE_ALIASES = ['prune']
SORT_ALIASES = ['sort']

def build_alias_lookups (): 
    mk_map = lambda x: {alias:x[0] for alias in x}
    result = {}
    result.update (mk_map (NAME_ALIASES))
    result.update (mk_map (START_ALIASES))
    result.update (mk_map (COMPLETED_ALIASES))
    result.update (mk_map (DUE_ALIASES))
    result.update (mk_map (FLAGGED_ALIASES))
    result.update (mk_map (NEXT_ALIASES))
    result.update (mk_map (TYPE_ALIASES))
    result.update (mk_map (NOTE_ALIASES))
    result.update (mk_map (STATUS_ALIASES))
    return result

def build_date_alias_lookups (): 
    mk_map = lambda x: {alias:x[0] for alias in x}
    result = {}
    result.update (mk_map (START_ALIASES))
    result.update (mk_map (COMPLETED_ALIASES))
    result.update (mk_map (DUE_ALIASES))
    return result

def build_string_alias_lookups (): 
    mk_map = lambda x: {alias:x[0] for alias in x}
    result = {}
    result.update (mk_map (NAME_ALIASES))
    result.update (mk_map (TYPE_ALIASES))
    result.update (mk_map (NOTE_ALIASES))
    result.update (mk_map (STATUS_ALIASES))
    return result
    
ALIAS_LOOKUPS = build_alias_lookups ()

DATE_ALIAS_LOOKUPS = build_date_alias_lookups ()

STRING_ALIAS_LOOKUPS = build_string_alias_lookups ()

# TOKENS
SPACE = 'SP'
TEXT = 'TXT'
QUOTED_TEXT = 'QTXT'
OPEN_BRACE = 'OB'
CLOSE_BRACE = 'CB'
NOT_EQUAL = 'NE'
EQUAL = 'EQ'
DOUBLE_QUOTE = 'DQ'
SINGLE_QUOTE = 'SQ'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'
BACKSLASH = 'BS'

TOKEN_PATTERNS = [
          # tok name, pattern, text equivalent
          (OPEN_BRACE, re.compile('^(\()')),
          (CLOSE_BRACE, re.compile('^(\))')),
          (AND, re.compile('^(and)(\(| )')),
          (OR, re.compile('^(or)(\(| )')),
          (SPACE, re.compile('^( )')),
          (DOUBLE_QUOTE, re.compile('^(")')),
          (SINGLE_QUOTE, re.compile("^(')")),
          (EQUAL, re.compile('^(=)')),
          (NOT_EQUAL, re.compile('^(!=)')),
          (NOT, re.compile('^(!)')),
          (BACKSLASH, re.compile('^(\\\\)'))
          ]

ESCAPEABLE_CHARS = '"\\'


BOOL_TYPE = 'Boolean'
DATE_TYPE = 'Date'
STRING_TYPE = 'String'

def read_to_end_quote (quote_char,remainder):
    text = ""
    escaped = False
    while len (remainder) > 0:
        char = remainder[0]
        remainder = remainder[1:]
        if escaped:
            if char in ESCAPEABLE_CHARS:
                text += char
            else:
                text += '\\'
                text += char
            escaped = False
        else:
            if char == '\\':
                escaped = True
            elif char == quote_char:
                return (text, remainder)
            else:
                text += char 
    assert False, "unclosed quote"
            

def tokenise (characters):
    remainder = characters
    text = ""
    tokens = []
    while len (remainder) > 0:
        matched = False
        for tok_name, cpattern in TOKEN_PATTERNS:
            if len (remainder) > 0 and not matched:
                match = cpattern.match (remainder)
                if match != None:
                    tok_value = match.group(1)
                    LOGGER.debug ("remainder: %s", remainder)
                    matched = True
                    if len (text) > 0:
                        tok = (TEXT, text)
                        LOGGER.debug ("token: %s flushed", tok)
                        tokens.append (tok)
                        text = ''
                    if tok_name == DOUBLE_QUOTE or tok_name == SINGLE_QUOTE:
                        string, remainder = read_to_end_quote (tok_value, remainder[1:])
                        tok = (QUOTED_TEXT, string)
                        LOGGER.debug ("token: %s quoted", tok)
                        tokens.append (tok)
                    else:
                        remainder = remainder[len(tok_value):]
                        tok = (tok_name, tok_value)
                        LOGGER.debug ("token: %s matched", tok)
                        tokens.append (tok)
        if not matched:
            LOGGER.debug ("remainder: %s", remainder)
            text += remainder[0]
            remainder = remainder[1:]
        
    if len (text) > 0:
        tok = (TEXT, text)
        LOGGER.debug ("token: %s final flush", tok)
        tokens.append (tok)

    tokens = [token for token in tokens if token[0] != SPACE]                  
    LOGGER.debug ("tokens: %s", tokens)
    return tokens

def next_token (tokens, options):
    if len(tokens) == 0:
        assert False, 'end of tokens, expected ' + str(options)
    t,v = tokens[0]
    if not t in options:
        assert False, 'found "' + v + '" not: ' + str(options)
    return (t,v), tokens[1:]
    
def parse_string (tokens, stop_tokens):
    buf = []
    while len(tokens) > 0:
        t,v = tokens[0]
        tokens = tokens[1:]
        if t in stop_tokens:
            return unicode(''.join(buf)), [(t,v)] + tokens
        else:
            buf.append(v)
    return unicode(''.join(buf)), []

def and_fn (lhs_fn, rhs_fn, x):
    
    lhs = lhs_fn (x)
    LOGGER.debug ('eval and: lhs=(%s)', lhs)
    assert type(lhs) == bool
    if not lhs:
        return False;
    
    rhs = rhs_fn (x)
    LOGGER.debug ('eval and: rhs=(%s)', rhs)
    assert type(lhs) == bool
    return rhs

def or_fn (lhs_fn, rhs_fn, x):
    lhs = lhs_fn (x)
    LOGGER.debug ('eval or: lhs=(%s)', lhs)
    assert type(lhs) == bool, "expected " + BOOL_TYPE + ' but got ' + str(type(lhs))
    if lhs:
        return True;
    
    rhs = rhs_fn (x)
    LOGGER.debug ('eval or: rhs=(%s)', rhs)
    assert type(lhs) == bool
    return rhs

def reorder (lhs, rhs):
    if type (rhs) == datetime:
        return rhs,lhs
    if type (lhs) == tuple:
        return rhs, lhs
    return lhs, rhs
    
def eq_fn (lhs, rhs):
    lhs, rhs = reorder (lhs, rhs)
    LOGGER.debug ('eval =: (%s) = (%s)', lhs, rhs)
    
    if type(rhs) == tuple:
        LOGGER.debug ('eval 1 =: (%s) = (%s)', lhs, rhs)
        result = match_date_against_range (lhs, rhs)
    elif (lhs == None and rhs != None) or (lhs != None and rhs == None):
        LOGGER.debug ('eval 2 =: (%s) = (%s)', lhs, rhs)
        result= False
    elif type(lhs) == type(rhs):
        if type(lhs) == str or type(lhs) == unicode: 
            LOGGER.debug ('eval 3 =: (%s) = (%s)', lhs, rhs)
            result = re.search(rhs, lhs) != None
        else:
            LOGGER.debug ('eval 4 =: (%s) = (%s)', lhs, rhs)
            result = lhs == rhs
    elif type(rhs) == tuple:
        LOGGER.debug ('eval 5 =: (%s) = (%s)', lhs, rhs)
        result = match_date_against_range (lhs, rhs)
    else:
        assert False, 'unknown or incompatible types: ' + str(type(lhs)) + ' and ' + str(type(rhs))
    
    LOGGER.debug ('result =: (%s)', result)
    return result

def ne_fn (lhs, rhs):
    LOGGER.debug ('eval !=: (%s) != (%s)', lhs, rhs)
    result = not eq_fn (lhs, rhs)
    LOGGER.debug ('result !=: (%s)', result)
    return result

def adapt (x):
    if type (x) == str:
        return unicode (x)
    if isinstance (x,Note):
        return x.get_note()
    return x

def access_field (x, field):
    if not field in x.__dict__:
        LOGGER.debug ('accessing field %s.%s - not in dict, returning None', type(x), field)
        return None
    result = x.__dict__[field]
    result = adapt (result)
    LOGGER.debug ('accessing field %s.%s=\'%s\'', type(x), field, result)
    return adapt (result)

def parse_expr (tokens, type_required=BOOL_TYPE, now = now (), level = 0):
    LOGGER.debug ('parsing %s tokens: %s', level, tokens)
    tok, tokens = next_token (tokens, [TEXT, QUOTED_TEXT, NOT, OPEN_BRACE])
    (t,v) = tok
    
    # NOT
    if t == NOT:
        assert type_required == BOOL_TYPE, "expecting a ' + required_type' expression, not " + BOOL_TYPE
        expr, tokens, expr_type, expr_string = parse_expr (tokens, now=now, level=level+1)
        assert expr_type == BOOL_TYPE, "not must have a boolean argument"
        LOGGER.debug ('built %s:1 %s %s', level, expr_type, expr_string)
        return (lambda x: not expr (x)), tokens, BOOL_TYPE, 'not(' + expr_string + ')'
    
    # LHS
    if t == TEXT and v =='true':
        lhs = lambda x: True
        lhs_string = 'true'
        lhs_type = BOOL_TYPE
    elif t == TEXT and v =='false':
        lhs = lambda x: False
        lhs_string = 'true'
        lhs_type = BOOL_TYPE
    elif t == TEXT and v in ALIAS_LOOKUPS:
        field = ALIAS_LOOKUPS[v]
        lhs = lambda x: access_field(x, field)
        lhs_string = 'field:' + field
        if field in DATE_ALIAS_LOOKUPS:
            lhs_type = DATE_TYPE
        elif field in STRING_ALIAS_LOOKUPS:
            lhs_type = STRING_TYPE
        else:
            lhs_type = BOOL_TYPE
    elif t == OPEN_BRACE:
        lhs, tokens, lhs_type, lhs_string = parse_expr (tokens, now=now, level=level+1)
        tokens = next_token (tokens, [CLOSE_BRACE])[1]
    elif t == QUOTED_TEXT:
        text = v
        lhs = lambda x: unicode (text)
        lhs_string = '"' + v + '"'
        lhs_type = STRING_TYPE
        if type_required == DATE_TYPE:
            rng = process_date_specifier (now, text)
            lhs = lambda x: rng
            lhs_string = '[' + date_range_to_str(rng) + ']'
            lhs_type = DATE_TYPE
    elif t == TEXT:
        text = v
        lhs = lambda x: unicode (text)
        lhs_string = text
        lhs_type = STRING_TYPE
        if type_required == DATE_TYPE:
            rng = process_date_specifier (now, text)
            lhs = lambda x: rng
            lhs_string = '[' + date_range_to_str(rng) + ']'
            lhs_type = DATE_TYPE
    else:
        assert False, 'unexpected token: ' + v
    
    LOGGER.debug ('built %s:2 %s %s', level, lhs_type, lhs_string)
    
    # OPERATOR 
    if len(tokens) == 0:
        LOGGER.debug ('built %s:3 %s %s', level, lhs_type, lhs_string)
        assert type_required == lhs_type, "expecting a " + type_required + ' got a ' + lhs_type + ': ' + lhs_string
        return lhs, tokens, lhs_type, lhs_string
    
    tok, tokens = next_token (tokens,[AND, OR, EQUAL, NOT_EQUAL, CLOSE_BRACE])
    op,v = tok
    if op == CLOSE_BRACE:
        LOGGER.debug ('built %s:4 %s %s', level, lhs_type, lhs_string)
        assert type_required == lhs_type, "expecting a " + type_required + ' got a ' + lhs_type + ': ' + lhs_string
        return lhs, [tok] + tokens, lhs_type, lhs_string
        
    rhs, tokens, rhs_type, rhs_string = parse_expr (tokens, type_required = lhs_type, now=now, level=level+1)         
    assert lhs_type == rhs_type, "incompatible types, " + lhs_type + ' ' + rhs_type

    assert type_required == BOOL_TYPE, "expecting a " + type_required + ' but got ' + BOOL_TYPE

    if op == AND:
        expr_string = '(' + lhs_string + ')AND(' + rhs_string + ')' 
        LOGGER.debug ('built %s:5 %s %s', level, BOOL_TYPE, expr_string)
        return (lambda x: and_fn(lhs, rhs, x)), tokens, BOOL_TYPE, expr_string
    elif op == OR:
        expr_string = '(' + lhs_string + ')OR(' + rhs_string + ')' 
        LOGGER.debug ('built %s:6 %s %s', level, BOOL_TYPE, expr_string)
        return (lambda x: or_fn(lhs, rhs, x)), tokens, BOOL_TYPE, expr_string
    elif op == EQUAL:
        expr_string = '(' + lhs_string + ')=(' + rhs_string + ')' 
        LOGGER.debug ('built %s:7 %s %s', level, BOOL_TYPE, expr_string)
        return (lambda x: eq_fn (lhs (x), rhs (x))), tokens, BOOL_TYPE, expr_string 
    elif op == NOT_EQUAL:
        expr_string = '(' + lhs_string + ')!=(' + rhs_string + ')' 
        LOGGER.debug ('built %s:8 %s %s', level, BOOL_TYPE, expr_string)
        return (lambda x: ne_fn (lhs (x), rhs (x))), tokens, BOOL_TYPE, expr_string 

def get_date_attrib_or_now (item, attrib):
    if not attrib in item.__dict__:
        return FAR_FUTURE
    result = item.__dict__[attrib]
    if result == None:
        return FAR_FUTURE
    return result

def make_command_filter (expr_str):    
    # First look for sort/prune
    bits = re.split(' ', expr_str)
    if len (bits) >= 2:
        cmd = bits[0].strip()
        if cmd in PRUNE_ALIASES:
            assert len (bits) == 2, 'prune takes one node type argument, got: ' + expr_str
            typ = bits[1].strip ()
            if typ == 'any' or typ == 'all':
                return Prune ([PROJECT, CONTEXT, FOLDER]) # NOT TASKS!!!
            assert typ in [PROJECT, CONTEXT, FOLDER], 'no such node type in prune: ' + typ
            return Prune ([typ])
        if cmd in FLATTEN_ALIASES:
            assert len (bits) == 2, 'flatten takes one node type argument, got: ' + expr_str
            typ = bits[1].strip ()
            if typ == 'any' or typ == 'all':
                return Flatten ([TASK, PROJECT, CONTEXT, FOLDER])
            assert typ in [TASK, PROJECT, CONTEXT, FOLDER], 'no such node type in flatten: ' + typ
            return Flatten ([typ])
        elif cmd in SORT_ALIASES:
            assert len (bits) == 3, 'sort takes two arguments, node type and field, got: ' + expr_str
            typ = bits[1].strip()
            if typ == 'any' or typ == 'all':
                types = [TASK, PROJECT, CONTEXT, FOLDER]
            else:
                assert typ in [TASK, PROJECT, CONTEXT, FOLDER], 'no such node type in sort: ' + typ
                types = [typ]
            field = bits[2].strip()
            assert field in ALIAS_LOOKUPS, 'no such sortable field:' + field
            field = ALIAS_LOOKUPS.get(field)
            if field in DATE_ALIAS_LOOKUPS:
                get_date = lambda x: get_date_attrib_or_now (x, field)
                return Sort (types, get_date, field)
            else:
                get_field = lambda x: x.__dict__[field]
                return Sort (types, get_field, field)
    return None

def make_expr_filter (expr_str, include):
    match_fn, tokens_left, expr_type, expr_string = parse_expr (tokenise (expr_str), now=now())
    if len (tokens_left) > 0:
        assert False, 'don\'t know what to do with: ' + str (tokens_left)
    assert expr_type == BOOL_TYPE, "filter must have a boolean argument"
    return Filter ([TASK, PROJECT, CONTEXT, FOLDER], match_fn, include, expr_string)

def make_filter (expr_str, include):
    
    filtr = make_command_filter (expr_str)
    if filtr == None:
        filtr = make_expr_filter (expr_str, include)
    return filtr

            
