# ofexport V1.0.4 #

- [Changelog](https://github.com/psidnell/ofexport/blob/master/CHANGELOG.md)

Avenues for help/abuse:

- [Wiki](https://github.com/psidnell/ofexport/wiki)
- [Bugs](https://github.com/psidnell/ofexport/issues)
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

        ofexport -i Work --tci "this week" -o ~/Desktop/doc.taskpaper --open

will produce a TaskPaper document on your desktop containing all items completed this week related to "Work" and open it (if you have TaskPaper installed).

### Example Uses ###

- Generating project/time specific reports.
- Creating web content.
- Exporting key tasks to devices/OSs that don't support OmniFocus via Dropbox.
- Backing up the OmniFocus database to a form searchable by other tools.
- Automatically creating reports on demand with Hazel whenever OmniFocus writes its database.

### Features

**Export to a number of text based file formats:**

- TaskPaper
- Plain Text
- Markdown/FoldingText
- OPML (Can be read by OmniOutliner, various MindMap tools)
- HTML

**Filter what gets exported:**

- Include/exclude tasks, projects and folders with text searches (regular expressions)
- Include/exclude tasks and projects by flag state.
- Include/exclude, tasks and projects by start/completion/due date.

**Restructure the data:**

- Flatten the outport document to create a simpler document (just projects containing tasks)
- Sort tasks by completion date or projects by name.
- Eliminate empty projects/folders.
- Organise by project or context hierarchy.

**Open**

- **ofexport** is built on a re-useable python library.
- You can use this in your own tools.
- The code is licenced under the [Apache License](http://opensource.org/licenses/Apache-2.0)

**Planned Features**

- Custom template based formatting for document types.
- "Tagging related" features.

### Limitations ###

Given that ofexport is using a completely undocumented and unsupported means of accessing the OmniFocus database, there are inevitably some shortcomings. The tool doesn't all the metadata you might expect from the OmniFocus database such as:

- Context Status (I don't know where it's in the database yet)
- Notes/attachments (I'm not completely sure how these are encoded yet)
- Project Type/Status (I don't know they're stored is in the database yet)

### WARNINGS ###

If you don't know what a bash script is, have never used the command line or don't know what a correct $PATH variable looks like then reading on is probably just going to give you a headache.

If Omni change the format of their database in a future update then of export will need to be fixed.

Also, this program reads your OmniFocus database file directly. While it should be impossible (as written) for it to modify or delete that database, set fire to your Mac, empty your bank accounts or knock the earth out of orbit - bugs happen. But you obviously have backups - right?  

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
		
To get help on usage and the full list of options, run the command with no arguments:-

        ofexport

A simple example of usage is:-

        ofexport -o report.txt

This produces a not particularly useful and possibly huge text file (report.txt) of your entire task database.

To get useful data out we want to start using more structured file formats and filters.

### File Formats:

The format of the report file is controlled by the suffix of the output file. So by running:

        ofexport -o report.txt

you'll get a text file. By changing the suffix you'll get different formats:

- .txt or .text: a simple text file
- .md or .markdown: a Markdown file
- .ft or .foldingtext: a Folding Text document (the same as .md)
- .tp or .taskpaper: a taskpaper document
- .opml: an OPML document
- .html or .htm: an HTML document			 

### Project or Context Mode ###

By default tasks are organised by project. By selecting **-C** the tool will instead organise by context. Usage of **-P** and **-C** can be used between filters to change the nature of the filtering. Whichever mode the tool is in at the end of the filtering dictates whether project or context mode is used to format the output.

### Filters

Filters are a powerful way of controlling the content or structure of your report.

Filters generally have two forms: **include** and **exclude**.

We'll be referring to the following structure:

    Folder: Home
        Project: Cat
                Task: Feed the cat junk
                Task: Train Tiddles to juggle
    Folder Work
        Project: Mail
                Task: Send receipts
                Task: Purge junk
 
#### Include Filters

When an include filter matches an item then it (and it's descendants, and all items to the root) will appear in the report. All other items will be eliminated.

If you ran an include filter searching for "Work" you'd get:

    Folder Work
        Project: Mail
                Task: Send receipts
                Task: Purge junk

If you ran a filter searching for "junk" you'd get:

    Folder: Home
        Project: Cat
                Task: Feed the cat junk
    Folder Work
        Project: Mail
                Task: Purge junk

If you ran a filter searching for "Cat" you'd get:

    Folder: Home
        Project: Cat
                Task: Feed the cat junk
                Task: Train Tiddles to juggle
 
#### Exclude Filters ####

When an exclude filter matches an item then it (and it's descendants) will not in the report. All other items will be retained.

If you ran an exclude filter searching for 'junk' you'd get:

    Folder: Home
        Project: Cat
                Task: Train Tiddles to juggle
    Folder Work
        Project: Mail
                Task: Send receipts
 
If you ran an exclude filter searching for ''Cat" you'd get:

    Folder: Home
    Folder Work
        Project: Mail
                Task: Send receipts
                Task: Purge junk

#### Filter List ####

**Generic**

        -i regexp: include anything matching regexp
        -e regexp: exclude anything matching regexp
        --si spec: include anything with start matching spec
        --se spec: exclude anything with start matching spec
        --ci spec: include anything with completion matching spec
        --Fi: include anything flagged
        --Fe: exclude anything flagged

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

        --Ci regexp: include contexts matching regexp
        --Ce regexp: exclude contexts matching regexp

**Misc**

        -F: flatten project/task structure
        --prune: Remove empty projects/folders

#### Multiple Filters ####

The important thing to note about filters is that you can specify as many as you like and they are executed in the order you specify. If there are multiple filters then the output of one is passed to the next and so on.

So you might start by including only your work folder, then exclude any project with "Routine" in the title, then include only items completed today.

It's possible to create quite sophisticated queries on your OmniFocus database by using a series of includes, excludes and regular expressions but even without an in-depth knowledge of what a regular expressions is, it's possible to achieve white a lot.

It's possible to change between project and context mode by adding **-P** or **-C** between filters. The tools's final mode dictates how the report is printed. It's also possible to run all the filters in project mode and flip to context mode just for the output or vice versa. 

### Filtering on Dates:

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

#### Pruning ####

You might run a filter that eliminates a lot of tasks and leaves a lot of empty projects or folders in your report. If you don't want to see these then use the prune option.

### Examples:

This produces a document containing all tasks completed yesterday from any folder with "Work" in it's title:
	
        ofexport -o report.tp --fi Work --tci 'yesterday' --prune --open
	
This uses a little regular expression magic to create a document containing all tasks completed today from any folder with the exact name "Work":
	
        ofexport -o report.tp --fi '^Work$' --tci 'today' --prune --open
	
This produces a document containing all tasks completed today from any folder that does NOT have "Work" in it's title:
	
        ofexport -o report.tp --fe Work --tci 'today' --prune --open

This uses a little regular expression magic to create a document containing all tasks completed today from any folder with the exact name "Work" or "Home".
	
        ofexport -o report.tp --fi '^Work$|^Home$' --tci 'today' --prune --open

This produces a document containing all tasks completed today from any folder with "Work" in it's title and the flattens/simplifies the indenting:
	
        ofexport -o report.tp --fi Work --tci 'today' --prune -F --open

This produces a report showing all tasks that contain "Beth" and their enclosing projects:-
			
        ofexport -o report.tp -i 'Beth' --prune --open -F

This produces the report of what I have yet to do on this project			

        ofexport -o TODO.md --open --pi 'OmniPythonLib Todo' -F --tci none

### Tips and Tricks ###

- If you're generating a TaskPaper file you can include @tags in your task text and they'll be recognised by TaskPaper when it loads the fie.
- Add filters one at a time and see what happens. Add the flatten/prune filters last since they can make it hard to diagnose why you're getting unexpected items in your output.

### Pitfalls ###

**Seeing things you don't expect in the report:** This happens a lot with task groups. If you create a filter to show all completed tasks then you'll get them in your report - and all their children even if they are completed. That's the way filters are designed. This seems intuitive for folders (show me everything in X) but less so here. If you then flatten the report you'll see a mix of completed/uncompleted tasks and probably assume it's a bug (which is arguable). You might want to consider flattening before filtering on completion or alternatively including all completed tasks then excluding uncompleted tasks. Nobody said it was easy.

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

