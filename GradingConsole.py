import tkinter as tk
from tkinter import ttk, font



class GradeCalculator(tk.Tk):


    def __init__(self):
        super().__init__()
        
        
        self.set_theme()

        self.title("Grade Calculator")
        self.total_pts_lost = 0
        self.context_menu = None

        # List to store entered grades
        self.grades = []

        # Listbox to display grades
        self.grade_listbox = tk.Listbox(self, width=10, height=10)
        self.grade_listbox.grid(row=0, column=0, padx=10, pady=10)

        # Entry widget to input grades
        self.grade_entry = ttk.Entry(self, width=10)
        self.grade_entry.grid(row=1, column=0, padx=10, pady=10)

        # Button to add grade
        self.add_button = ttk.Button(self, text="Add", command=self.add_grade)
        self.add_button.grid(row=2, column=0, padx=10, pady=10)


        inner_frame = tk.Frame(self, bd=2, relief=tk.SOLID)
        inner_frame.grid(row=0, column=1, padx=10, pady=10)


        # Label to display point totals
        self.lost_label = tk.Label(inner_frame, text="Pts Lost: 0.0", fg="red")
        self.lost_label.grid(row=0, column=0, padx=10)
        self.earned_label = tk.Label(inner_frame, text="Pts Earned: 0.0", fg="green")
        self.earned_label.grid(row=1, column=0, padx=10)

        # Entry widget to input total points possible
        self.pts_possible_entry = tk.Entry(self, width=10)
        self.pts_possible_entry.grid(row=1, column=1, padx=10, pady=10)
        self.pts_possible_entry.insert(0, "Pts Possible")
        self.pts_possible_entry.config(fg='grey')  # Change text color to grey

        #cfont = tk.Font(size=12, weight="bold")
        self.per_label = ttk.Label(self, text="Score", font=("Arial", 14, "bold"))
        self.per_label.grid(row=2, column=1, padx=10, pady=10)


        # Bind the stuff for the pts_possible and it's "hint"
        self.pts_possible_entry.bind("<FocusIn>", lambda event=None: self.on_pts_possible_entry_click())
        self.pts_possible_entry.bind("<FocusOut>", lambda event=None: self.on_pts_possible_entry_leave())
        self.pts_possible_entry.bind("<KeyRelease>", lambda event=None: self.update_score())


        # Bind the Enter key to the Add Grade button
        self.bind('<Return>', lambda event=None: self.add_grade())
        self.bind('<KP_Enter>', lambda event=None: self.add_grade())


        # Bind the ListBox so user can right-click to delete / clear
        self.grade_listbox.bind("<Button-3>", lambda event: self.on_listbox_right_click(event))
        self.grade_listbox.bind("<Button-1>", lambda event: self.destroy_menu())
        
        


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

        self.context_menu = ttk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self.del_item)
        self.context_menu.add_command(label="Delete All", command=self.clear)
        self.context_menu.post(event.x_root, event.y_root)

        self.update_score()
    
    def set_theme(self):
        #style = ttk.Style()
        #print("themes: " + str(style.theme_names()))
        
        #self.tk.call("source", "winxpblue/winxpblue.tcl")
        self.tk.call("source", "adapta/adapta.tcl")
        #self.tk.call("set_theme", "dark")
        ttk.Style().theme_use("adapta")
        
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
            self.pts_possible_entry.config(fg='black')  # Change text color to black


    def on_pts_possible_entry_leave(self):
        if self.pts_possible_entry.get() == "":
            self.pts_possible_entry.delete(0, "Pts Possible")
            self.pts_possible_entry.config(fg='grey')  # Change text color to black
        else:
            self.update_score()


    def update_score(self):
        try:
            pts_possible = float(self.pts_possible_entry.get())
        except:
            print("Please input total points possible!")
            return

        etotal = pts_possible - self.total_pts_lost
        self.earned_label.config(text=f"Pts Earned: {etotal:.2f}")


        percentage = (etotal/pts_possible) * 100
        self.per_label.config(text="--Score--\n%.2f/%.2f = %.3f%%" % (etotal, pts_possible, percentage))
        #self.per_label.config(font=(self.per_label['font'].actual()['family'], self.per_label['font'].actual()['size'] + 2, "bold"))



        # Clear the entry for the next input
        self.grade_entry.delete(0, tk.END)

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

