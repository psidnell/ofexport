# Usage Examples

This produces a document containing all tasks completed last week from any folder with "Work" in it's title:
    
        ofexport -f=Work -t "done='last week'" -a prune -o /tmp/ex1-work-last-week.taskpaper
    
This uses a little regular expression magic to create a document containing all tasks completed today from any folder with the exact name "Home":
    
        ofexport -f='^Home$' -t done='today' -a prune -o /tmp/ex2-home-today.taskpaper
    
This produces a document containing all tasks completed today from any folder that does NOT have "Work" in it's title:
    
        ofexport -E -f=Work -I -a prune -o /tmp/ex3-not-work-today.taskpaper

This uses a little regular expression magic to create a document containing all tasks completed today from any folder with the exact name "Work" or "Home".
    
        ofexport -f='^Work$|^Home$' -t done='today' -a prune -o /tmp/ex4-work-or-home-today.taskpaper

This produces a document containing all tasks completed this week from any folder with "Work" in it's title and the flattens/simplifies the indenting:
    
        ofexport -f=Work -t 'done="this week"' -a prune -a flatten -o /tmp/ex5-work-this-week-flat.taskpaper

This produces a report showing all tasks that contain "Beth" and their enclosing projects:
            
        ofexport -a=Beth -a prune -a flatten -o /tmp/ex6-Beth.taskpaper

This produces the report of what I have yet to do on this project           

        ofexport -f flatten -p="'ofexport Todo'" -E -t done=any -o /tmp/ex7-ofexport-todo.taskpaper

This produces the report of all uncompleted tasks that are flagged or due soon

        ofexport -E -a done=any -I -t "flagged or (due='to tomorrow')" -o /Users/psidnell/Desktop/ex7-ofexport-todo.taskpaper
                

