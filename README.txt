Introduction
------------

Comments welcome (twitter: @psidnell)

The GitHub repo is here: https://github.com/psidnell/omnifocus

I've wanted a reasonably flexible way of generating mardown/taskpaper/html reports of completed tasks from OmniFocus - but never quite found any love for AppleScript.

So I've developed a python library that directly reads the OF database and builds a complete model of the task/project/context hierarchy that can then be used to generate whatever you wish.

It's early days at the moment (there's no help at all yet) but there are example report generating scripts (for my purposes) that should get you going if you know python and sample AppleScript wrappers so you can add buttons that drive the scripts from the OF toolbar.

I've been using this for a few months now with no issues, but bear in mind that the problem of this approach (i.e. scraping the database) is that Omni make no guarantees about compatibility or support going forward. And nor do I :-)

Pro's/Con's
-----------
+ Omnifocus doesn't need to be running (or even installed!) as long as it's db file is present.
- If Omni change their schema then the code will need fixing.

Files:
------
To see if everything works run 'python of_to_html.py'. This will print out your whole task hierarchy to OF.html on your desktop.

omnifocus.py - the core library, has a main that prints the whole repository to the console
of_to_html.py - renders the whole library as HTML
of_to_opml.py - renders the whole library as OPML
of_to_md.py - renders the whole library as Markdown
of_to_tp.py - renders the whole library as Taskpaper
of_to_text.py - renders the whole library as Text
days.py (DEPRECATED) - a report generation library that prints completed tasks in any of the above formats.
ofexport.py - a general purpose export and filtering utility

About ofexport
--------------

Run without arguments to print full option list and examples.
