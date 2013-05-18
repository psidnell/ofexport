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

from treemodel import Visitor, Project, Context, TASK, PROJECT, FOLDER
import logging
import sys

logging.basicConfig(format='%(asctime)-15s %(name)s %(levelname)s %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.ERROR)

INCLUDED='INCLUDED'
EXCLUDED='EXCLUDED'
PATH_TO_INCLUDED='PATH_TO_INCLUDED'

def set_attrib_to_root (path_to_root, name, value):
    for item in path_to_root:
        item.attribs[name] = value

def mark_branch_not_marked (item, project_mode):
    if item.marked:
        item.marked = False
        if (item.type == TASK or item.type == PROJECT) and not project_mode:
            # We only got here because we recursed from a context
            # Tasks/Projects are not a tree in context mode, they're flat so we don't want
            # to un-mark all the children since they might be in a different context
            return
        for child in item.children:
            mark_branch_not_marked (child, project_mode)
            
class BaseFilterVisitor(Visitor):
    def __init__(self, include=True):
        self.filter = None
        self.include = include
        self.traversal_path = []
    def begin_any (self, item):
        # Can't use the item parent since this only has meaning
        # in project mode - have to track our own traversal path
        parent = None
        if len(self.traversal_path) > 0:
            parent = self.traversal_path[-1]
        item.attribs[PATH_TO_INCLUDED] = False
        if parent != None:
            # Inherit these attribute
            item.attribs[INCLUDED] = parent.attribs[INCLUDED]
            item.attribs[EXCLUDED] = parent.attribs[EXCLUDED]
            assert parent.attribs[INCLUDED] != None, "missing attribute in " + parent.name
            assert parent.attribs[EXCLUDED] != None, "missing attribute in " + parent.name
        else:
            item.attribs[INCLUDED] = False
            item.attribs[EXCLUDED] = False
        self.traversal_path.append(item)
    def end_any (self, item):
        assert item.attribs[PATH_TO_INCLUDED] != None, "missing attribute in " + item.name
        assert item.attribs[INCLUDED] != None, "missing attribute in " + item.name
        assert item.attribs[EXCLUDED] != None, "missing attribute in " + item.name
        self.traversal_path.pop()
        if self.include and not (item.attribs[INCLUDED] or item.attribs[PATH_TO_INCLUDED]):
            mark_branch_not_marked (item, self.project_mode)
        # We've finished processing the node, tidy up
        # and avoid confusing the next filter.
        del (item.attribs[INCLUDED])
        del (item.attribs[EXCLUDED])
        del (item.attribs[PATH_TO_INCLUDED])
    def match_required (self, item):
        if item.attribs[INCLUDED] or item.attribs[EXCLUDED]:
            # The decision has already been made
            return False
        return True
    def set_item_matched (self, item, matched):
        # invoked from begin_XXX
        if self.include:
            if matched:
                # Then we want this node in the output and want to stop
                # this filter testing removing any parents or children of this node
                item.attribs[INCLUDED] = True
                set_attrib_to_root (self.traversal_path, PATH_TO_INCLUDED, True)
        else: # In exclude mode
            if matched:
                # This node is toast
                mark_branch_not_marked (item, self.project_mode)
            else:
                # We haven't excluded it so it stays
                pass

def includes (include):
    if include:
        return 'include'
    else:
        return 'exclude'
    
class Filter(BaseFilterVisitor):
    def __init__(self, types, match_fn, include, nice_string):
        BaseFilterVisitor.__init__(self, include)
        self.types = types
        self.match_fn = match_fn
        self.nice_string = nice_string
    def begin_any (self, item):
        BaseFilterVisitor.begin_any (self, item)
        if item.type in self.types and self.match_required(item):
            matched = self.match_fn(item)
            if matched:
                logger.debug ("matched id:%s %s %s", item.id, item.type, item.name)
            self.set_item_matched(item, matched);
    def __str__(self):
        return includes (self.include) + ' ' + str(self.types) + ' where ' + self.nice_string


class Sort(Visitor):
    def __init__(self, types, get_key_fn, nice_string):
        Visitor.__init__(self)
        self.types = types
        self.get_key_fn = get_key_fn
        self.nice_string = nice_string
    def begin_any (self, item):
        if item.type in self.types:
            logger.debug ("sorting id:%s %s %s", item.id, item.type, item.name)
            item.children = self.sort_list(item.children)
    def sort_list (self, items):
        return sorted(items, cmp=self.compare)
    def compare (self, x, y):
        # Use the key we've been asked to use but
        # try other comparators to get at least a deterministic
        # ordering
        diff = self.cmp (self.get_key_fn (x), self.get_key_fn (y))
        if diff == 0:
            diff = self.cmp (x.order, y.order);
        if diff == 0:
            diff = self.cmp (x.id, y.id)
        return diff;
    def cmp (self, l, r):
        if l < r:
            return -1
        if l > r:
            return 1
        return 0
    def __str__(self):
        return 'Sort ' + str(self.types) + ' by ' + self.nice_string

class Prune (Visitor):
    def __init__(self, types):
        Visitor.__init__(self)
        self.types = types
    def end_any (self, item):
        if item.type in self.types:
            logger.debug ("pruning candidate id:%s %s", item.id, item.name)
            self.prune_if_empty(item)
    def prune_if_empty (self, item):
        if item.marked:
            empty = len ([x for x in item.children if x.marked]) == 0
            if empty:
                logger.debug ("pruning id:%s %s", item.id, item.name)
                item.marked = False
    def __str__ (self):
        return 'Prune ' + str(self.types)

class Flatten (Visitor):
    def __init__(self, types):
        Visitor.__init__(self)
        self.types = types
    def end_any (self, item):
        self.flatten (item)
    def flatten (self, item):
        logger.debug ("flattening candidate L1 id:%s %s %s", item.id, item.type, item.name)
        new_children = []
        for child in item.children:
            if child.type in self.types:
                logger.debug ("flattening candidate L2 id:%s %s %s", child.id, child.type, child.name)
                for grandchild in list(child.children):
                    logger.debug ("flattening candidate L3 id:%s %s %s", grandchild.id, grandchild.type, grandchild.name)
                    if grandchild.type == child.type or child.type == FOLDER:
                        logger.debug ("flattening id:%s %s %s", grandchild.id, grandchild.type, grandchild.name)
                        new_children.append(grandchild)
                        child.children.remove (grandchild)
            new_children.append(child)
        item.children = []
        for child in new_children:
            item.add_child (child)
    def __str__ (self):
        return 'Flatten' + str(self.types)
    
class Tasks (Visitor):
    def __init__(self, root_folder, root_context):
        Visitor.__init__(self)
        self.root_folder = root_folder
        self.root_context = root_context
        self.project = Project (name='Tasks')
        self.context = Context (name='Tasks')
    def end_project (self, item):
        for child in item.children:
            self.project.add_child(child)
        item.children = []
    def end_folder (self, item):
        if item == self.root_folder:
            self.root_folder.children = []
            self.root_folder.add_child(self.project)
    def end_context (self, item):
        if item != self.root_context:
            for child in item.children:
                if child.type == TASK:
                    self.context.add_child(child)
            item.children = []
        else:
            self.root_context.children = []
            self.root_context.add_child(self.context)
    def __str__ (self):
        return 'Tasks'