import tkinter as tk

def do_something():
    print("Something was selected from the menu")

# Create the main window
root = tk.Tk()
root.title("Drop-down Menu Example")

# Create a menu bar
menubar = tk.Menu(root)

# Create a menu
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=do_something)
file_menu.add_command(label="Open", command=do_something)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Add the menu to the menu bar
menubar.add_cascade(label="File", menu=file_menu)

# Display the menu bar
root.config(menu=menubar)

# Run the application
root.mainloop()
