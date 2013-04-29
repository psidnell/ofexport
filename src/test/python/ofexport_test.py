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

from ofexport import fix_abbrieviated_expr

class Test_fmt_datematch(unittest.TestCase):
    
    def test_fix_abbrieviated_expr (self):
        self.assertEquals ('(type=Project) and (name=x)', fix_abbrieviated_expr ('Project', '=x'))
        self.assertEquals ('(type=Project) and (name!=x)', fix_abbrieviated_expr ('Project', '!=x'))
        self.assertEquals ('name=x', fix_abbrieviated_expr ('any', '=x'))
        self.assertEquals ('name!=x', fix_abbrieviated_expr ('all', '!=x'))
        self.assertEquals ('prune Task', fix_abbrieviated_expr ('Task', 'prune'))
        self.assertEquals ('prune any', fix_abbrieviated_expr ('any', 'prune'))
        self.assertEquals ('prune all', fix_abbrieviated_expr ('all', 'prune'))
        self.assertEquals ('sort Folder text', fix_abbrieviated_expr ('Folder', 'sort'))
        self.assertEquals ('sort Folder due', fix_abbrieviated_expr ('Folder', 'sort due'))