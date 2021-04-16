README

Shapes 'R' Us POS System

How to set up and use the system:
    
0. Download all source files into the same directory
1. Build the database from the supplied sql script
2. Modify the contents of secret_data.py to fit with your DBMS settings
3. Run interface.py using the command python3 interface.py in a console working in this directory
4. You will be prompted for login credentials. *only valid employees can use the system
5. After a succesful login the main menu will appear, and the user can select from a variety of commands using the displayed keys, and this menu will be shown after each command until Exit is selected.
5a. There is a hidden command key 'R' that will allow the user to reset their database back to its original state. This command is only available in the main menu, and not under any sub-menus. 
6. Changes made to the database are made as the program runs, so the user may exit from the console at any point without fear of damaging or losing their data.
6a. If you exit manually halfway through a transaction your cart will not be saved.
