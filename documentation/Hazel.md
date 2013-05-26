# Hazel Integration

## Rules

Currently OmniFocus keeps it's database in one of two places, depending on how it was purchased:

* Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2
* Library/Caches/com.omnigroup.OmniFocus.MacAppStore/OmniFocusDatabase2

Add the correct path as a watched directory in Hazel and then set up the rules:

![Web Page](HazelRules.png)

Here I have attempted to avoid the rule being run too frequently or too quickly after OmniFocus has saved the file to avoid the script running when I'm doing a lot work in OmniFocus. If the script runs too busily it can slow your machine down and cause OmniFocus problems by holding a lock on it's database for long periods. This recipe seems to be a workable compromise.

## Script

![Web Page](HazelRulesScript.png)

Scripts run from Hazel don't necessarily execute in the same environment as your command line - depending on how your environment is set up. Most of my environment customisations are in my .bashrc so in the above I load that environment and then run my custom script using it's explicit path to avoid issues.
