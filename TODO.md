# V2.1.0

# V2.1.2

- What else to put in this release?
- Still further performance gains to be made in template processing (cache formatted attribs)
- probe deeper into the metadata for statuses?
- useability - any quick wins? command line shortcuts? -DF? canned filters?
- Can I determine next/available?

# Backlog

- Command Line
    - Select input database location - necessary for OmniFocus 2 alpha testing
- Database
    - What about task availability? Where is it stored?
    - Try ofexport with OF 2
    - Where are inbox items stored in in the OF DB?
        Can I catch them with "No Context"
    - Can I detect a if a project/context is paused?
- Attributes
    - "type" should be a template variable
    - $date and $time variables in templates
    - Add item depth as filterable parameter
- Templates
    - Have a default template in code such that an empty template file still works
    - Put file extension associations in the templates
- Bug: unexpected arguments error prints whole line, not just bad arg
- Sorting
    - Add "natural" sort - i.e. sort by the order from the OF DB (this is done initially already)
- Documentation
    - Write up geektool integration - create section on integration with other tools - by objective e.g. tasks on the desktop, add to features - SCREENSHOT
    - Document How I use it
    - document any new filter variables
- Architecture
    - Assertions to prevent mis-wiring of type hierarchies
    - More general config - e.g. global date format?
    - A filter that prepends type to items - for debugging
    - Scan for #xxx in the text and add tp tag?
    - Filter to merge projects folders etc if they have same name?
    - Allow +-3d, 2w etc?
    - Dump OF schema programatically
    - Create a taggable dump of projects as files with links to corresponing Omnifocus entities - for hazel and openmeta scripts
        file format: fld-fld-…-proj
    - Read other file types such as Taskpaper/OPML (done json)
    - Resolve utf8/ascii issues - not sure what's going on - redirecting stdout "changes things" as does invocation from applescript?!?!?!
    - look for OFEXPORT_HOME in the environment first
- Testing
    - test all the assertions properly with unit tests (done most of them)
    - Install it myself separately from my dev environment
    - Update the paths accordingly
