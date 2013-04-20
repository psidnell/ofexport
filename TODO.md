# ofexport Todo

* V1.0.6
    * Use json i/o for integration testing
    * move html/opml preamble into visitors
    * Summary filter
    * Add config dir
    * ofexport can use OFEXPORT_HOME to find it's config dir
    * Bring templates forward?
* Backlog
    * Document How I use it
    * from == since in dates? maybe tokenise properly
    * Try ofexport with omnifocus 2
    * Where are inbox items stored in in the OF DB?
    * A visitor to prepend type to items - for debugging
    * Assertions to prevent mis-wiring of type hierarchies
    * proper logging: with on/off on the command line
    * merge projects folders etc if they have same name?
    * Make command line parsing more robust - how?
    * Allow "weekend", "weekday" in date ranges
    * I don't like the command line parsing, would like +/- switches for include exclude, beyond what getopt can do - I have a sneaky idea
    * Json output
    * Allow +-3d, 2w etc
    * Select input database location
    * Extra config from a file? environment variables? OFEXPORT_HOME
    * Templates for document types
    * Configurable formatting for printers? "stylesheets"?
    * Named tagging strategies? (or rely on templates)
    * What tags to include in taskpaper, due? start? context?
    * Scan for #xxx in the text and add tp tag?
    * Links (from persistent identifier)
    * Dump OF schema programatically
    * Extract note text (even possible?)
    * Create a taggable dump of projects as files with links to corresponing Omnifocus entities - for hazel and openmeta scripts
    * Read other file types such as Taskpaper?
    * Resolve utf8/ascii issues - not sure what's going on - redirecting stdout "changes things"?!?!?!
    * Can I detect a if a project is paused?

