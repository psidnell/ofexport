Introduction
------------

I've wanted a reasonably flexible way of generating mardown/taskpaper/html reports of completed tasks from OmniFocus - but never quite found any love for AppleScript.

So I've developed a python library that directly reads the OF database and builds a complete model of the task/project/context hierarchy that can then be used to generate whatever you wish.

It's early days at the moment (there's no help at all yet) but there are example report generating scripts (for my purposes) that should get you going if you know python and sample AppleScript wrappers so you can add buttons that drive the scripts from the OF toolbar.

I've been using this for a few months now with no issues, but bear in mind that the problem of this approach (i.e. scraping the database) is that Omni make no guarantees about compatibility or support going forward. And nor do I :-)

Usage:
------
To see if everything works run 'python omnifocus.py'. Assuming your omnifocus
library is in the same place as mine it'll print out your whole task hierarchy.

omnifocus.py - the core library, has a main that prints the whole repository to the console
of_to_links.py - renders the whole library as HTML
of_to_opml.py - renders the whole library as OPML
days.py - a report generation library that prints md, opml, html, taskpaper or folding text report
          of completed tasks. This makes all sorts of assumptions about naming that probably
          only applies to me, but a little modification I'm sure it'll work for you too.

The other python files re-use omnifocus.py and produce custom reports. These are tailored to my own needs
but should be enough to get you going.

There are also some AppleScript wrappers that can you can use in omnifocus so you can drive your scripts from the toolbar.

Comments welcome.

The freshly minted GitHub repo is here: https://github.com/psidnell/omnifocus

TODO:
-----
- Make days.py more useful to people who aren't me.
- Decode note xml, may not be simple (are attachments uuencoded in them?).
- Add more help for any unfortunate soul who tries to use this.
