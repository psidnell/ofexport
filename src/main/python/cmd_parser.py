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

TOKEN_PATTERNS = [
          # tok name, pattern, text equivalent
          ('TXT', '\\\\"', '"'),
          ('TXT', "\\\\'", "'"),
          ('OB', '\(', '('),
          ('CB', '\)', ')'),
          ('NE', '!=', '!='),
          ('EQ', '=', '='),
          ('DQ', '"', '"'),
          ('SQ', "'", "'"),
          ('AND', 'and', 'and'),
          ('OR', 'or', 'or'),
          ('NOT', 'not', 'not'),
          ('BS', '\\\\', '\\')
          ]

def sub_tokenise (tokens, tok_name, pattern, equiv):
    result = []
    for typ, val in tokens:
        if typ == 'UNK':
            pieces = re.split (pattern, val)
            if len (pieces) > 1:
                result.append ((typ, pieces[0]))
                pieces = pieces [1:]
                for piece in pieces:
                    result.append ((tok_name, equiv))
                    result.append ((typ, piece))
            else:
                result.append ((typ, val))
        else:
            result.append ((typ, val))
    return result
        
def tokenise (cmd):
    tokens = [('UNK',cmd)]
    for tok_name, pattern, equiv in TOKEN_PATTERNS:
        tokens = sub_tokenise (tokens, tok_name, pattern, equiv)
    result = []
    # Anything we haven't recognised is text
    for t,v in tokens:
        if t == 'UNK':
            if v != '':
                result.append(('TXT', v))
        else:
            result.append ((t, v))
    return result