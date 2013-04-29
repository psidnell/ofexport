# Usage Examples

ofexport -f='^Test' -C -c="^Test" -o src/test/data/db-5.json

This produces a document containing all tasks completed last week from any folder with "Worms" in it's title:
    
        ofexport -f=Worms -t "done='last week'" -a prune -o /tmp/ex1-worms-last-week.taskpaper 

This uses a little regular expression magic to create a document containing all tasks completed today from any folder with the exact name "Ham":
    
        ofexport -f='^Ham$' -t done='today' -a prune -o /tmp/ex2-ham-today.taskpaper 
   
This produces a document containing all tasks completed today from any folder that does NOT have "Worms" in it's title:
    
        ofexport -E -f=Worms -a prune -o /tmp/ex3-not-worms.taskpaper 

This uses a little regular expression magic to create a document containing all tasks completed today from any folder with the exact name "Work" or "Home".
    
        ofexport -f='^Worms$|^Ham$' -t done='today' -a prune -o /tmp/ex4-worms-or-ham-today.taskpaper 

This produces a document containing all tasks completed this week from any folder with "Worms" in it's title and the flattens/simplifies the indenting:
    
        ofexport -f=Worms -a flatten -a prune -o /tmp/ex5-work-this-week-flat.taskpaper 

This produces the report of what I have yet to do on this project           

        ofexport -f flatten -p="'ofexport Todo'" -E -t done=any -o /tmp/ex7-ofexport-todo.taskpaper 

This produces the report of all uncompleted tasks that are flagged or due soon

        ofexport -E -a done=any -I -t "flagged or (due='to tomorrow')" -o /tmp/ex8-due-or-flagged.taskpaper 


