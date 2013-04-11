# Ofexport Command: #


## Overview:

**ofexport** is a command line utility that reads the OmniFocus database. It's a work in progress but currently it's capabilities include:-

Exports it to a number of text based file formats:

- Taskpaper
- Text
- Markdown
- OPML
- HTML

Filter what gets exported:

- Include/exclude tasks, projects, contexts and folders with text searches (regular expressions)
- Include/exclude tasks and projects by completion date (regular expressions and "human" ones)

Perform some restructuring of the data:

- Flatten the outport document to create a simpler document (just projects containing tasks)
- Sort by various criteria

## Installation:
		
- Write this ("it's just python") @todo

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

        ofexport -o TODO.md --open --pi 'OmniPythonLib Todo' -F
