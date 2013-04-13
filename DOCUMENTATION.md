# ofexport Command: #

Avenues for abuse:

- [Blog: Poor Signal](http://poor-signal.blogspot.co.uk)
- [Twitter: @psidnell](http://twitter.com/psidnell)

Related Applications:

- [OmniFocus](http://www.omnigroup.com/products/omnifocus/)
- [OmniFocus Extras ofexport Forum Thread](http://forums.omnigroup.com/showthread.php?t=29081)
- [Taskpaper](http://www.hogbaysoftware.com/products/taskpaper)
- [TaskPaper ofexport Forum Thread](https://groups.google.com/forum/?fromgroups=#!topic/taskpaper/7xQ4lE_1O9I)
- [Hazel](http://www.noodlesoft.com/hazel.php)
- [Dropbox](http://www.dropbox.com)

## Overview:

**ofexport** is a command line utility that reads and exports the task database from the OmniFocus application.

For example:

        ofexport --fi '^Work' --tci 'this week' --prune -o ~/Desktop/doc.taskpaper --open

will produce a TaskPaper document on your desktop containing all items completed this week from your work folder and open it (if you have TaskPaper installed).

### Example Uses ###

- Generating project/time specific reports.
- Exporting key tasks to devices/OSs that don't support OmniFocus via Dropbox.
- Backing up the OmniFocus database to a form searchable by other tools.
- Automatically creating reports on demand with Hazel

### Features

**Export to a number of text based file formats:**

- TaskPaper
- Plain Text
- Markdown/FoldingText
- OPML (Can be read by OmniOutliner, various MindMap tools)
- HTML

**Filter what gets exported:**

- Include/exclude tasks, projects, contexts and folders with text searches (regular expressions)
- Include/exclude tasks and projects by completion date (regular expressions and "human" ones)

**Perform some restructuring of the data:**

- Flatten the outport document to create a simpler document (just projects containing tasks)
- Sort by various criteria

**Open**

- **ofexport** is built on a re-useable python library.
- You can use this in your own tools.
- The code is licenced under the [Apache License](http://opensource.org/licenses/Apache-2.0)

**Coming Soon**

- Custom formatting for document types.
- "Tagging related" features.

## Download/Installation:

This pre-supposes a certain familiarity with the command line.

- The source is on [github](https://github.com/psidnell/ofexport).
- Download the [zip file](https://github.com/psidnell/ofexport/archive/master.zip).
- Double click on the zip file to unpack it.
- Rename and move the folder to wherever you want it to live.
- Edit the **ofexport** script and change the path to reflect the correct new location of  your files.
- From the command line set execute permission on "of export"
- Add the installation directory to your path.
- Run **ofexport** from the command line, if all is well then it should print it's help.
- If it doesn't then all is not well and I have failed you.

## Tutorial:
		
To get help on usage and the full list of options ,run the command with no arguments:-

        ofexport

A simple example of usage is:-

        ofexport -o report.txt

This produces a not particularly useful text file (report.txt) of your entire task database.

To get useful data out we want to start using more structured formats and filters.

### File Formats:

The format of the report file is controlled by the suffix of the output file. So by running:-

        ofexport -o report.txt

you'll get a text file. By changing the suffix you'll get different formats:-
- .txt or .text: a simple text file
- .md or .markdown: a Markdown file
- .ft or .foldingtext: a Folding Text document (the same as .md)
- .tp or .taskpaper: a taskpaper document
- .opml: an OPML document
- .html or .htm: an HTML document			 

### Filters:

Filters are a powerful way of controlling the content or structure of your report. A minimal useful example is:-

        ofexport -o report.tp --open --tci 'this week' --prune

This exports everything you've completed this week to a taskpaper document (report.tp) and opens it. The --tci and --prune options are both examples of filters.

In this case, the --tci filter (task completion include) includes only those tasks that were completed this week, eliminating all others. The resultant document would probably have a lot of empty folders and projects in it (because so many tasks have been filtered out). The  --prune filter eliminates any and all projects and folders that contain no tasks. The resultant document should be a pretty readable summary of what you've completed this week.

The core filters are:-

**Projects**

        --pi regexp: include projects matching regexp
        --pe regexp: exclude projects matching regexp
        --psi spec: include projects with start matching spec
        --pse spec: exclude projects with start matching spec
        --pci spec: include projects with completion matching spec
        --pce spec: exclude projects with completion matching spec
        --pdi spec: include projects with due matching spec
        --pde spec: exclude projects with due matching spec
        --pfi: include flagged projects
        --pfe: exclude flagged projects

**Tasks**

        --ti regexp: include tasks matching regexp
        --te regexp: exclude tasks matching regexp
        --tsi spec: include tasks with start matching spec
        --tse spec: exclude tasks with start matching spec
        --tdi spec: include tasks with due matching spec
        --tde spec: exclude tasks with due matching spec
        --tci spec: include tasks with completion matching spec
        --tce spec: exclude tasks with completion matching spec
        --tfi: include flagged tasks
        --tfe: exclude flagged tasks
        --tsc: sort tasks by completion

**Folders**

        --fi regexp: include folders matching regexp
        --fe regexp: exclude folders matching regexp

**Contexts**

        --ci regexp: include contexts matching regexp
        --ce regexp: exclude contexts matching regexp

**Misc**

        -F: flatten project/task structure

The important thing to note about filters is that you can specify as many as you like and they are executed in the order you specify.

It's possible to create quite sophisticated queries on your OmniFocus database by using a series of queries and regular expressions but even without an in-depth knowledge of what a regular expression is it's possible to achieve white a lot.

Filters respect the tree structure of the tasks in your OmniFocus database. Filters are applied to all the items (folders, tasks, projects or contexts) in your database. When the filter is applied to an item, if it matches then it and all it's descendent's will appear in the output report. If the match fails on an item then that item (and all it's descendants) are eliminated from the output report.

If there are multiple filters then the output of one is passed to the next and so on.

Most of the filters come in two flavours, include and exclude with one being the inverse of the other.

Filters are type specific: if you use a folder filter to include or exclude a folder and you have projects at the root level then the filter will ignore it and it will appear in your report.

### Filtering on Dates:

The core date format is YYYY-MM-DD (sorry America) largely because Taskpaper requires this format so that sorting works (I may provide configuration in the future).

A week is considered to start on Monday.

A specific day can be expressed as:

- "Monday" - the monday that occurs within this week.
- "th" - Days of the week can be abbreviated down to 2 characters.
- "yesterday", "today",  "tomorrow"
- "last tuesday" - the Tuesday that occurs in the previous week.
- "next sat" - the Saturday that occurs in the next week.
-  "2013-04-09"

A range of dates can be expressed as:

- "July", "jul" - every day in July of this year.
- "to 2013-05-10" - everything on or before the date.
- "from yesterday" - everything on or after yesterday.
- "yesterday to 2014-10-01" everything between the two days
- "this week" - everything from this Monday to this Sunday.
- "next week"
- "last week"
- "none" or "" - only matches items with no date
- "any" - only matches items with a date
	
### Examples:

This produces a document containing all tasks completed today from any folder with "Work" in it's title:-
	
        ofexport -o report.tp --fi Work --tci 'today' --prune --open
	
This uses a little regular expression magic to create a document containing all tasks completed today from any folder with the exact name "Work":-
	
        ofexport -o report.tp --fi '^Work$' --tci 'today' --prune --open
	
This produces a document containing all tasks completed today from any folder that does NOT have "Work" in it's title:-
	
        ofexport -o report.tp --fe Work --tci 'today' --prune --open

This uses a little regular expression magic to create a document containing all tasks completed today from any folder with the exact name "Work" or "Home".
	
        ofexport -o report.tp --fi '^Work$|^Home$' --tci 'today' --prune --open

This produces a document containing all tasks completed today from any folder with "Work" in it's title and the flattens/simplifies the indenting:-
	
        ofexport -o report.tp --fi Work --tci 'today' --prune -F --open

This produces a report showing all tasks that contain "Beth" and their enclosing projects:-
			
        ofexport -o report.tp --ti 'Beth' --prune --open -F

This produces the report of what I have yet to do on this project			

        ofexport -o TODO.md --open --pi 'OmniPythonLib Todo' -F --tci none

### Tips and Tricks ###

- If you're generating a TaskPaper file you can include @tags in your task text and they'll be recognised by Taskpaper when it loads the fie.
- Add filters one at a time and see what happens. Add the flatten/prune filters last since they can make it hard to diagnose why you're getting unexpected items in your output.

### Pitfalls ###

**Seeing things you don't expect in the report:** This happens a lot with task groups. If you create a filter to show all completed tasks then you'll get them in your report - and all their children even if they are completed. That's the way filters are designed. This seems intuitive for folders (show me everything in X) but less so here. If you then flatten the report you'll see a mix of completed/uncompleted tasks and probably assume it's a bug (which is arguable). You wight want to consider flattening before filtering on completion or alternatively including all completed tasks then excluding uncompleted tasks. Nobody said it was easy.

# License #

    Copyright 2013 Paul Sidnell

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

