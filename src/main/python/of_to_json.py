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
import json
import codecs
from datetime import datetime
from treemodel import Visitor, Context, Project, Task, Folder, CONTEXT, PROJECT, TASK, FOLDER

TIME_FMT = "%Y-%m-%d %H:%M:%S"

def save_attrib (item, attrib, attribs, convert):
    if not attrib in item.__dict__:
        return
    value = item.__dict__[attrib]
    if value == None:
        return
    attribs[attrib] = convert (value)

def load_attrib (item, attrib, attribs, convert):
    if not attrib in attribs:
        return
    value = attribs[attrib]
    item.__dict__[attrib] = convert (value)

class ConvertStructureToJsonVisitor(Visitor):
    def begin_any (self, item):
        if self.is_in_applicable_mode (item) and not 'id' in item.attribs:
            myid = str(uuid.uuid1())
            item.attribs['id'] = myid
            node_json_data = {'id' : myid }
            save_attrib (item, 'name', node_json_data, lambda x : x)
            save_attrib (item, 'type', node_json_data, lambda x : x)
            save_attrib (item, 'date_completed', node_json_data, lambda x: x.strftime (TIME_FMT))
            save_attrib (item, 'date_to_start', node_json_data, lambda x: x.strftime (TIME_FMT))
            save_attrib (item, 'date_due', node_json_data, lambda x: x.strftime (TIME_FMT))
            save_attrib (item, 'flagged', node_json_data, lambda x : x)
            item.attribs['json_data'] = node_json_data
    def end_task (self, item):
        self.add_children(item)
    def end_project (self, item):
        self.add_children(item)
    def end_folder (self, item):
        self.add_children(item)
    def end_context (self, item):
        children_json_data = []
        for child in item.children:
            if child.marked and 'id' in child.attribs:
                child_json_data = child.attribs['json_data']
                if child.type == CONTEXT:
                    children_json_data.append(child_json_data)
                else:
                    # The name is just a debugging aid
                    children_json_data.append({'ref' : child.attribs['id'], 'name' : child.name })
        item.attribs['json_data']['children'] = children_json_data
    def is_in_applicable_mode (self, item):
        # Project ,ode items are written first,
        # Contexts second with refs to tasks/projects
        if self.project_mode:
            return item.type in (FOLDER, PROJECT, TASK)
        else:
            return item.type == CONTEXT
    def add_children (self, item):
        if self.is_in_applicable_mode (item):
            children_json_data = []
            for child in item.children:
                if child.marked:
                    child_json_data = child.attribs['json_data']
                    children_json_data.append(child_json_data)
            item.attribs['json_data']['children'] = children_json_data

def load_from_json (json_data, item_db):
    if 'ref' in json_data:
        item = item_db[json_data['ref']]
        return item
    
    item_type = json_data['type']
    item_id = json_data['id']
    if item_type == FOLDER:
        item = Folder ()
    elif item_type == CONTEXT:
        item = Context ()
    elif item_type == TASK:
        item = Task ()
    elif item_type == PROJECT:
        item = Project ()
    load_attrib (item, 'name', json_data, lambda x: x)
    load_attrib (item, 'date_completed', json_data, lambda x: datetime.strptime (x, TIME_FMT))
    load_attrib (item, 'date_to_start', json_data, lambda x: datetime.strptime (x, TIME_FMT))
    load_attrib (item, 'date_due', json_data, lambda x: datetime.strptime (x, TIME_FMT))
    load_attrib (item, 'flagged', json_data, lambda x: x)
    
    for child_data in json_data['children']:
        child = load_from_json (child_data, item_db)
        item.add_child(child)

    item_db[item_id] = item
    return item

def read_json (file_name):
    instream=codecs.open(file_name, 'r', 'utf-8')
    json_data = json.loads(instream.read())
    instream.close ()
    
    item_db = {}
    root_project = load_from_json (json_data[0], item_db)
    root_context = load_from_json (json_data[1], item_db)
    
    
    
    return root_project, root_context
    
    