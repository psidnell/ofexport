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

class TypeOf(object):
    def __init__(self, name, thetype):
        self.thetype = thetype
        self.name = name
    def __get__(self, instance, owner):
        if self.name in instance.__dict__:
            return instance.__dict__[self.name]
        return None
    def __set__(self, instance, value):
        if value != None:
            assert isinstance (value, self.thetype), self.name + ': expected type ' + str(self.thetype) + ' got ' + str (value.__class__)
        instance.__dict__[self.name] = value