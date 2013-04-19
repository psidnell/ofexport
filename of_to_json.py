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
import uuid
from treemodel import Visitor, CONTEXT

TIME_FMT = "%Y-%m-%d %H:%M:%S"
def copy_attrib (item, attrib, attribs, convert):
    if not attrib in item.__dict__:
        return
    value = item.__dict__[attrib]
    if value == None:
        return
    attribs[attrib] = convert (value)


class ConvertStructureToJsonVisitor(Visitor):
    def begin_any (self, item):
        myid = str(uuid.uuid1())
        item.attribs['id'] = myid
        node_json_data = {'id' : myid }
        copy_attrib (item, 'name', node_json_data, lambda x : x)
        copy_attrib (item, 'type', node_json_data, lambda x : x)
        copy_attrib (item, 'date_completed', node_json_data, lambda x: x.strftime (TIME_FMT))
        copy_attrib (item, 'date_to_start', node_json_data, lambda x: x.strftime (TIME_FMT))
        copy_attrib (item, 'date_due', node_json_data, lambda x: x.strftime (TIME_FMT))
        copy_attrib (item, 'flagged', node_json_data, lambda x : x)
        
        item.attribs['json_data'] = node_json_data
    def end_task (self, item):
        for child in item.children:
            child_json_data = child.attribs['json_data']
            child_json_data['parent'] = item.attribs['id']
    def end_project (self, item):
        for child in item.children:
            child_json_data = child.attribs['json_data']
            child_json_data['parent'] = item.attribs['id']
    def end_folder (self, item):
        for child in item.children:
            child_json_data = child.attribs['json_data']
            child_json_data['parent'] = item.attribs['id']
    def end_context (self, item):
        for child in item.children:
            child_json_data = child.attribs['json_data']
            if child.type == CONTEXT:
                child_json_data['parent'] = item.attribs['id']
            else:
                child_json_data['context'] = item.attribs['id']
    def end_any (self, item):
        children_json_data = []
        for child in item.children:
            child_json_data = child.attribs['json_data']
            children_json_data.append(child_json_data)
        item.attribs['json_data']['children'] = children_json_data
        
    