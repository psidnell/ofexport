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

from treemodel import traverse_list, Visitor
from omnifocus import build_model, find_database
import os
import codecs

'''
Experimental!!!!

A db directory must exist on your desktop first
 
Creates a bazillion little html files each of which links/redirects back to an OmniFocus project/folder/context.
I'm wondering if I can use openmeta on them to essentially get tags into OF via the back door.

If I extract #tags from the item text then I can put that in the file and autotag can find it

'''
class GenerateTagDBVisitor(Visitor):
    def begin_folder (self, folder):
        self.generate_entry ('folder',  folder)
    def begin_project (self, project):
        self.generate_entry ('task', project)
    def begin_context (self, context):
        self.generate_entry ('context', context)
    def generate_entry (self, link_type, item):
        if 'persistentIdentifier' in item.ofattribs:
            ident = item.ofattribs['persistentIdentifier']
            link = 'omnifocus:///' + link_type + '/' + ident
            base = item.name.replace('/','_').replace('\\','/').replace('\.', '_')
            
            file_name=os.environ['HOME'] + '/Desktop/db/' + base + ' ' + ident + '.html'
            out=codecs.open(file_name, 'w', 'utf-8')
            link = 'omnifocus:///' + link_type + '/' + ident
            print >>out, '<html>'
            print >>out, '<head>'
            print >>out, '<meta http-equiv="refresh" content="0; url=' + link + '">'
            print >>out, '</head>'
            print >>out, '<body>'
            print >>out, '<p><a href="' + link + '">' + self.escape(item.name) + '</a>'
            print >>out, '</body>'
            print >>out, '</html>'
            out.close ()
    def escape (self, val):
        return val.replace('"','&quot;').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

if __name__ == "__main__":

    root_projects_and_folders, root_contexts = build_model (find_database ())
    
    traverse_list (GenerateTagDBVisitor (), root_projects_and_folders)
    traverse_list (GenerateTagDBVisitor (), root_contexts, project_mode=False)