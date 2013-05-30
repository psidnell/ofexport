# Changes #

## 3.0.1 (?????)

- Made default format when printing to stdout configurable.
- Reformatted json config using "recommended" layout (bleh!) with a BBEdit plugin http://bbeditextras.org/wiki/index.php?title=Text_Filters
- Moved db search path into config.
- Added config for default "%of cal" directives.
- Fixed a bug where I wasn't using the persistentIdentifier as the task id.

## 3.0.0 (2013-05-27) If you're not feeling brave, wait for 3.0.1

- Introduced a plugin model.
- Changed format of templates to support plugins better.
- Added a global config file: ofexport.json for plugins and file associations.
- Add **id** and **type** attributes to a few templates.

## 2.1.6 (2013-05-20)

- Tweaks to date sorting so that items with no dates appear below those that do.

## 2.1.5 (2013-05-18)

- Tweaks to sort algorithm to return underlying order when selected attributes of two items are equal.
- Added a --tasks filter to eliminate everything but tasks grouped under a single Tasks project/context.

## 2.1.4 (2013-05-14)

- Updated the installation instructions and added **install.sh** as a post-download script.
- Fixes to markdown template "hashes" now an attribute.

## 2.1.3 (2013-05-13)

- Added next as a filterable attribute of tasks.

## 2.1.2 (2013-05-10)

- Added status of a project/context as a field that can be filtered on or used in a template.

## 2.1.1 (2013-05-08)

- Added ability to set the start/due time of a calendar entry separately from OF start/due.
- Bug fix to calendar allday feature where UTC adjustment could push calendar entry to wrong day.
- Improved ics formatting so OmniFocus link in URL field rather than DESCRIPTION - making it clickable.

## 2.1.0 (2013-05-05)

- Added Calendar (ics) export.
- Allowed filtering on note text.

## 2.0.3 (2013-05-03)

- Fix for a nasty performance bug relating to notes

## 2.0.2 (2013-05-03)

- Changed OPML format so note text appears as an OmniOutliner block note, not a sequence of sub-nodes.
- Bug fix: notes weren't being escaped in OPML or HTML leading to invalid format.

## 2.0.1 (2013-05-01)

- Added notes from the OmniFocus database.
- Better logging.
- Prints to standard out if no file specified.
- Resolved some utf-8 issues.

## 2.0.0 (2013-04-29)

- New expression parsing engine for complex queries.
- Thumbnails in the documentation.
- Added dateFormat to templates.
- Bugfixes.

## 1.1.0 (2013-04-21)

- Customisable templates for formatting the output.
- Big internal changes to support templates.
- Much improved tests.
- Added json as an output format.
- Added json as an alternative input format.

## 1.0.5 (2013-04-18) ##
- Fewer and more modular command line options.
- Big internal changes to the filter mechanism.
- Much simpler filter building from command line arguments.
- Added link mode (-l) to add links to OmniFocus from TaskPaper documents.
- Added tags for projects/contexts in TaskPaper report.
  
## 1.0.4 (2013-04-15) ##

- Added Context mode.
- Improved test script.
- Filter performance improvement.
- Improved flattening algorithm to work in Context mode.
- Added "No Context" context that all tasks without a context get added to.

## 1.0.3 (2013-04-13) ##

- Big reworking of filter logic to squash a design bug. 
- Added a alphabetic project/folder sorting filter.
- Added -i/-e simple filters that searches all text types.
- Added --Fi/--Fe simple filters that work on any flagged type.
- More documentation.

## 1.0.2 (2013-12) ##

- Added the Apache V2 License to the source and documentation.
- Fix a bug caused by allowing newlines in task titles.
- Improved the documentation

## 1.0.1 (2013-04-10) ##

- Extended date filters to recognise month names.
- Extended date filters to recognise "any" and "none" for date matching.
- Lots of extra testing and bug fixing around date matching.

## 1.0.0 (2013-04-09) ##

- Added task filters for flagged, start and due
- Added project filters for flagged, start, completion and due
- Reworking date logic to be more human allow "next tuesday", "last week" etc.
