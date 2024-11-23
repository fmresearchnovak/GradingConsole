#!/usr/bin/env python3

import platform
import tkinter as tk
from tkinter import ttk, font



class GradeCalculator(tk.Tk):


    def __init__(self):
        super().__init__()
        
        
        self.set_theme()
        self.title("Grade Calculator")
        self.total_pts_lost = 0
        self.context_menu = None
        self.iconphoto(False, tk.PhotoImage(file="gc_icon.png"))

        # List to store entered grades
        self.grades = []
        
        
        # Listbox to display grades
        self.grade_listbox = tk.Listbox(self, width=10, height=10)
        self.grade_listbox.grid(row=0, column=0, padx=10, pady=10)
        #self.grade_listbox.pack(side="left")
        sb = tk.Scrollbar(self, orient='vertical', command=self.grade_listbox.yview)
        #sb.pack(side="right", fill="y")
        #sb.grid(row=0, column=0, sticky=tk.NS)
        self.grade_listbox.config(yscrollcommand = sb.set)

        # Entry widget to input grades
        self.grade_entry = ttk.Entry(self, width=10)
        self.grade_entry.grid(row=1, column=0, padx=10, pady=10)
        self.grade_entry.insert(0, "Pts. Lost")

        # Button to add grade
        self.add_button = ttk.Button(self, text="Add", command=self.add_grade)
        self.add_button.grid(row=2, column=0, padx=10, pady=10)


        inner_frame = ttk.Frame(self, padding="10", relief=tk.SOLID)
        inner_frame.grid(row=0, column=1, padx=10, pady=10)
        

        # Entry widget to input total points possible
        self.pts_possible_entry = ttk.Entry(inner_frame, width=10, style="Grey.TEntry")
        self.pts_possible_entry.grid(row=0, column=0, padx=10, pady=10)
        self.pts_possible_entry.insert(0, "Pts Possible")

        
        # Label to display point totals
        self.lost_label = ttk.Label(inner_frame, text="Pts Lost: 0.0", style="Red.TLabel")
        self.lost_label.grid(row=1, column=0, padx=10)
        self.earned_label = ttk.Label(inner_frame, text="Pts Earned: 0.0", style="Green.TLabel")
        self.earned_label.grid(row=2, column=0, padx=10)
        
        
        #cfont = tk.Font(size=12, weight="bold")
        self.per_label = ttk.Label(inner_frame, text="Score", font=("Arial", 14, "bold"), anchor="center")
        self.per_label.grid(row=3, column=0, padx=10, pady=10)
        
        # Entry widget to do eval lines, this feature is a big security flaw!
        self.eval_entry = ttk.Entry(self, width=15)
        self.eval_entry.grid(row=2, column=1, padx=10, pady=10)
        self.eval_entry.insert(0, "Enter Equation and Press Enter!")


        # Bind the stuff for the pts_possible and it's "hint"
        self.pts_possible_entry.bind("<FocusIn>", lambda event=None: self.on_pts_possible_entry_click())
        self.pts_possible_entry.bind("<FocusOut>", lambda event=None: self.on_pts_possible_entry_leave())
        self.pts_possible_entry.bind("<KeyRelease>", lambda event=None: self.update_score())


        # Bind the Enter key to the Add Grade button
        self.bind('<Return>', self.enter_key_callback)
        self.bind('<KP_Enter>', lambda event=None: self.add_grade())


        # Bind the ListBox so user can right-click to delete / clear
        if (platform.system() == "Linux"):
            right_click_button = "<Button-3>"
        if (platform.system() == "Darwin"):
            right_click_button = "<Button-2>"
            
        self.grade_listbox.bind(right_click_button, lambda event: self.on_listbox_right_click(event))
        self.grade_listbox.bind("<Button-1>", lambda event: self.destroy_menu())
        
        
        
    def enter_key_callback(self, event):
        self.add_grade()
        self.python_bad_security_evaluation()


    def destroy_menu(self):
        if(self.context_menu != None):
            self.context_menu.destroy()
            self.context_menu = None

    def on_listbox_right_click(self, event):
        if(self.grades == []):
            return

        item_index = self.grade_listbox.nearest(event.y)

        if item_index != -1:
            # Right-clicked on a specific item
            item = self.grade_listbox.get(item_index)
            self.grade_listbox.selection_set(item_index)
            self.grade_listbox.activate(item_index)
            print(f"Right-clicked on item: {item}")

        else:
            # This never gets called!
            # Right-click on the Listbox itself
            print("Right-clicked on Listbox")


        self.destroy_menu()

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self.del_item)
        self.context_menu.add_command(label="Delete All", command=self.clear)
        self.context_menu.post(event.x_root, event.y_root)

        self.update_score()
    
    def set_theme(self):
        #style = ttk.Style()
        #print("themes: " + str(style.theme_names()))
        
        self.tk.call("source", "winxpblue/winxpblue.tcl")
        ttk.Style().theme_use("winxpblue")
        #self.tk.call("source", "adapta/adapta.tcl")
        #ttk.Style().theme_use("adapta")
        #self.tk.call("set_theme", "dark")

        ttk.Style().configure("Red.TLabel", foreground="red")
        ttk.Style().configure("Green.TLabel", foreground="green")
        ttk.Style().configure("Black.TEntry", foreground="black")
        ttk.Style().configure("Grey.TEntry", foreground="grey")

        #self.tk.call("set_theme", "dark")
        #style.theme_use("clam")
        #style.set_theme("clam")
        #self.set_theme()
        #self.set_theme(theme_name="arc")


    def del_item(self):
        selected_indices = self.grade_listbox.curselection()
        for index in selected_indices:
            self.grade_listbox.delete(index)
            del self.grades[index]
        self.update_score()


    def clear(self):
        self.grade_listbox.delete(0, tk.END)
        self.grades = []
        self.update_score()



    def on_pts_possible_entry_click(self):
        if self.pts_possible_entry.get() == "Pts Possible":
            self.pts_possible_entry.delete(0, tk.END)
            self.pts_possible_entry.config(style="Black.TEntry")  # Change text color to black


    def on_pts_possible_entry_leave(self):
        if self.pts_possible_entry.get() == "":
            self.pts_possible_entry.insert(0, "Pts Possible")
            self.pts_possible_entry.config(style="Grey.TEntry")  # Change text color to black
        else:
            self.update_score()
            
            
    def python_bad_security_evaluation(self):
        try:
            line = str(self.eval_entry.get())
            result = eval(line)
            result = str(result)
            #print(type(result))
            #print("result: ", result)
            #self.eval_entry.config(text=str(result))
            self.eval_entry.delete(0, tk.END) # delete current text
            self.eval_entry.insert(0, str(result)) # insert result
        except:
            print("failed to eval: " + str(self.eval_entry.get()))


    def update_score(self):
        # Clear the entry for the next input
        self.grade_entry.delete(0, tk.END)
        
        try:
            pts_possible = float(self.pts_possible_entry.get())
        except:
            print("Please input total points possible!")
            self.earned_label.config(text="Pts Earned: 0.0")
            self.per_label.config(text="Score")
            return

        etotal = pts_possible - self.total_pts_lost
        self.earned_label.config(text=f"Pts Earned: {etotal:.2f}")


        percentage = (etotal/pts_possible) * 100
        self.per_label.config(text="%.1f/%.1f = %.2f%%" % (etotal, pts_possible, percentage))
        #self.per_label.config(font=(self.per_label['font'].actual()['family'], self.per_label['font'].actual()['size'] + 2, "bold"))



    def add_grade(self):
        try:
            # Get the grade from the entry and convert it to a float
            grade = float(self.grade_entry.get())

        except ValueError:
            # Handle the case where the entered value is not a valid float
            print("Please enter a valid grade.")
            return

        # Add the grade to the list
        self.grades.append(grade)

        # Update the Listbox with the grades
        self.grade_listbox.delete(0, tk.END)
        for g in self.grades:
            self.grade_listbox.insert(tk.END, g)

        # Update the lost label
        self.total_pts_lost = sum(self.grades)
        self.lost_label.config(text=f"Pts Lost: {self.total_pts_lost:.2f}")

        self.update_score()




def blah(x):
    print(x)
    print("blah!")

        
if __name__ == "__main__":
    
    app = GradeCalculator()
    #app.bind_all("<Key>", blah)
    app.mainloop()

