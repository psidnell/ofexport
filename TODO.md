# V3.0.2

- Let it brew
- check inbox scanning
- Fwd: Hazel Rules for OmniFocus `ofexport` (SOLVED) - write this up
    From: Roger Sheen <infotexture@gmail.com>   Fwd: Hazel Rules for OmniFocus `ofexport` (SOLVED)
    From: Paul Sidnell <psidnell@yahoo.co.uk>   Re: Hazel Rules for OmniFocus `ofexport` (SOLVED)
    
    From: "Roger Sheen" <infotexture@gmail.com>
    Subject: Fwd: Hazel Rules for OmniFocus `ofexport` (SOLVED)
    Date: 31 May 2013 13:27:17 BST
    To: "Paul Sidnell" <psidnell@yahoo.co.uk>
    
    On Tuesday, 2013-05-28, at 12:28 CEST, Roger Sheen wrote:
    Hazel still refuses to run my script properly […] but at least I know that's a Hazel
    problem and I'll investigate further later this week.
    
    
    Hi Paul,
    
    I contacted the Hazel developer Paul Kim to find out why my `ofexport` script wouldn't work when run from Hazel and was able to trace it to the environment issues you encountered.
    
    I settled on a slightly different solution, but the problem is solved (see forwarded message below).
    
    One advantage to this approach is that it also works with `launchd` (in case people don't own Hazel). I'll try to write this up soon and send you a pull request so you can add it to the documentation if you like.
    
    The new plugin model in v3 looks like a very good idea
    
    Still haven't had time to test that, but looking forward to it.
    
    More soon,
    
    Roger
    
    
    
    Forwarded message:
    
    From: Roger Sheen <infotexture@gmail.com>
    To: Paul Kim <support@noodlesoft.com>
    Subject: Re: Hazel Rules for OmniFocus `ofexport` (SOLVED)
    Date: Fri, 31 May 2013 14:10:47 +0200
    
    On Thursday, 2013-05-30, at 23:44 CEST, Roger Sheen wrote:
    On Thursday, 2013-05-30, at 21:20 CEST, Paul Kim wrote:
    As for the script, you cannot assume the $PATH variable is set. Hazel runs scripts in a different environment than what you get when you run it in Terminal. I suggest writing out debugging output to a log file so you can get more details on how and where it's failing.
    
    Right, but shouldn't @psidnell's approach for sourcing the local environment fix that?
    
    
    Hi Paul,
    
    I found the problem. I was sourcing `~/.bash_profile`, whereas @psidnell used `~/.bashrc`.
    
    I guess Hazel invokes a new bash instance as a non-login shell, so `~/.bashrc` applies, but `~/.bash_profile` doesn't, since this is only executed for login shells [^1].
    
    (Perhaps this might be worth mentioning in the Hazel help or FAQ?)
    
    My environment variables are defined in `~/.bash_profile`, but not in `~/.bashrc`, so Hazel doesn't pick them up.
    
    When I copied the relevant `export` lines from `~/.bash_profile` to my custom script, it runs fine with a rule that calls it as an external script (via Other...), without having to use the embedded script to source the local environment first.
    
    	export OFEXPORT_HOME="/path/to/ofexport"
    	export PATH=$PATH:"$OFEXPORT_HOME/bin"
    
    Thanks for your help in troubleshooting--and thanks for Hazel!
    
    Regards,
    
    Roger
    
    
    
    ---
    
    [^1]:	<http://www.joshstaiger.org/archives/2005/07/bash_profile_vs.html>
    From: Paul Sidnell <psidnell@yahoo.co.uk>
    Subject: Re: Hazel Rules for OmniFocus `ofexport` (SOLVED)
    Date: 2 June 2013 19:02:26 BST
    To: Roger Sheen <infotexture@gmail.com>
    
    Thanks for that.
    
    Some areas of the Hazel documentation are a little "light" in detail!
    
    I'll Beef up this area of the doc next time I update i.
    
    Thanks,
    
    Paul
    
    On 31 May 2013, at 13:27, Roger Sheen <infotexture@gmail.com> wrote:
    
    On Tuesday, 2013-05-28, at 12:28 CEST, Roger Sheen wrote:
    Hazel still refuses to run my script properly […] but at least I know that's a Hazel
    problem and I'll investigate further later this week.
    
    
    Hi Paul,
    
    I contacted the Hazel developer Paul Kim to find out why my `ofexport` script wouldn't work when run from Hazel and was able to trace it to the environment issues you encountered.
    
    I settled on a slightly different solution, but the problem is solved (see forwarded message below).
    
    One advantage to this approach is that it also works with `launchd` (in case people don't own Hazel). I'll try to write this up soon and send you a pull request so you can add it to the documentation if you like.
    
    The new plugin model in v3 looks like a very good idea
    
    Still haven't had time to test that, but looking forward to it.
    
    More soon,
    
    Roger
    
    
    
    Forwarded message:
    
    From: Roger Sheen <infotexture@gmail.com>
    To: Paul Kim <support@noodlesoft.com>
    Subject: Re: Hazel Rules for OmniFocus `ofexport` (SOLVED)
    Date: Fri, 31 May 2013 14:10:47 +0200
    
    On Thursday, 2013-05-30, at 23:44 CEST, Roger Sheen wrote:
    On Thursday, 2013-05-30, at 21:20 CEST, Paul Kim wrote:
    As for the script, you cannot assume the $PATH variable is set. Hazel runs scripts in a different environment than what you get when you run it in Terminal. I suggest writing out debugging output to a log file so you can get more details on how and where it's failing.
    
    Right, but shouldn't @psidnell's approach for sourcing the local environment fix that?
    
    
    Hi Paul,
    
    I found the problem. I was sourcing `~/.bash_profile`, whereas @psidnell used `~/.bashrc`.
    
    I guess Hazel invokes a new bash instance as a non-login shell, so `~/.bashrc` applies, but `~/.bash_profile` doesn't, since this is only executed for login shells [^1].
    
    (Perhaps this might be worth mentioning in the Hazel help or FAQ?)
    
    My environment variables are defined in `~/.bash_profile`, but not in `~/.bashrc`, so Hazel doesn't pick them up.
    
    When I copied the relevant `export` lines from `~/.bash_profile` to my custom script, it runs fine with a rule that calls it as an external script (via Other...), without having to use the embedded script to source the local environment first.
    
    	export OFEXPORT_HOME="/path/to/ofexport"
    	export PATH=$PATH:"$OFEXPORT_HOME/bin"
    
    Thanks for your help in troubleshooting--and thanks for Hazel!
    
    Regards,
    
    Roger
    
    
    
    ---
    
    [^1]:	<http://www.joshstaiger.org/archives/2005/07/bash_profile_vs.html>
    
    

# Bugs

- None known at the moment...

# Backlog

- Command Line
    - Recipies/macros - names bundles of command line args
- Useability
    - useability - any quick wins? command line shortcuts? -DF? canned filters?
- Database
    - What about task availability? Where is it stored?
    - Try ofexport with OF 2
    - Where are inbox items stored in in the OF DB?
        Can I catch them with "No Context"
    - Can I detect a if a project/context is paused?
- Attributes
    - childcount as an attribute
    - Can I determine availability?
    - "type" should be a template variable
    - $date and $time variables in templates
    - Add item depth as filterable parameter
- Templates
    - Create a "dump" template that dumps everything.
    - Have a default template in code such that an empty template file still works
    - Put file extension associations in the templates
- Tag Clouds
    - Check out PyTagCloud
        https://github.com/atizo/PyTagCloud
    - Clouds myself: http://stackoverflow.com/questions/3180779/html-tag-cloud-in-python
- Integrations
    - Log to DayOne? - how?
- Sorting
    - Add "natural" sort - i.e. sort by the order from the OF DB (this is done initially already)
- Documentation
    - Write up geektool integration - create section on integration with other tools - by objective e.g. tasks on the desktop, add to features - SCREENSHOT
    - Document How I use it
    - document any new filter variables
- Architecture
    - Tips on perspectives and casting blobs - investigate
        forums.omnigroup.com/showthread.php?t=29538
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
- Releasing
    - Save released versions, tag? Make script
