# Changes #

## 1.0.5 (???) ##

- Added link mode (-l) to add links to omnifocus tasks in TaskPaper documents.
- Added generic --si/--se/--ci/--ce/--di/--de date filters that work on tasks and projects.
- Renamed context filter from --ci to --Ci to avoid option clash.
- Added tags to projects in TaskPaper report.
- More sorting options.
  
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
