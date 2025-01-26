from tkinter import *
from tkinter import ttk
import json
from tkinter import messagebox

class Todo:
    def __init__(self, root):
        self.root = root
        self.root.title('To-do List')
        self.root.geometry('650x410+300+150')
        self.root.config(bg='white')

        # Add header
        self.label = Label(self.root, text="To-Do List App", font="Arial 25 bold", width=10, bd=5, bg='greenyellow', fg="black")
        self.label.pack(side="top", fill=BOTH)

        # Add Task Label
        self.label2 = Label(self.root, text="Add Task", font="Arial 18 bold", width=10, bd=5, bg="#f39c12", fg="black")
        self.label2.place(x=40, y=60)

        # Tasks List Label
        self.label3 = Label(self.root, text='Tasks', font="Arial 18 bold", width=10, bd=5, bg="#f39c12", fg="black")
        self.label3.place(x=320, y=60)

        # Tasks Listbox
        self.main_text = Listbox(self.root, height=9, bd=5, width=23, font="Arial 20 italic bold")
        self.main_text.place(x=280, y=100)

        # Textbox to add tasks
        self.text = Text(self.root, bd=5, height=2, width=30, font="Arial 10 bold")
        self.text.place(x=40, y=100)

        # Add Task Button
        self.add_button = Button(self.root, text="Add Task", command=self.add, bg="green", fg="white", relief=SOLID, font=("Helvetica", 12, "bold"))
        self.add_button.place(x=40, y=220)

        # Delete Task Button
        self.delete_button = Button(self.root, text="Delete Task", command=self.delete, bg="red", fg="white", relief=SOLID, font=("Helvetica", 12, "bold"))
        self.delete_button.place(x=150, y=220)

        # Mark Task as Completed Button
        self.completed_button = Button(self.root, text="Mark as Completed", command=self.mark_completed, bg="blue", fg="white", relief=SOLID, font=("Helvetica", 12, "bold"))
        self.completed_button.place(x=40, y=260)

        # Search Bar
        self.search_bar = Entry(self.root, width=30)
        self.search_bar.place(x=40, y=300)

        # Load tasks from file
        self.load_tasks()

    def add(self):
        content = self.text.get(1.0, END).strip()
        if content:
            task = {'description': content, 'priority': 'None'}
            with open('tasks.json', 'a') as file:
                json.dump(task, file)
                file.write("\n")
            self.main_text.insert(END, content)
            self.text.delete(1.0, END)

    def delete(self):
        try:
            selected_task_index = self.main_text.curselection()[0]
            task = self.main_text.get(selected_task_index)
            result = messagebox.askyesno("Delete", f"Are you sure you want to delete the task: '{task}'?")
            if result:
                self.main_text.delete(selected_task_index)
                self.remove_from_file(task)
        except IndexError:
            pass

    def mark_completed(self):
        try:
            selected_task_index = self.main_text.curselection()[0]
            task = self.main_text.get(selected_task_index)
            
            # Option 1: Add a checkmark to the task to indicate completion
            completed_task = f"✔️ {task}"
            self.main_text.delete(selected_task_index)
            self.main_text.insert(selected_task_index, completed_task)
            
            # Option 2: Change the text color to green (uncomment if preferred)
            # self.main_text.itemconfig(selected_task_index, {'fg': 'green'})

        except IndexError:
            pass

    def remove_from_file(self, task_to_remove):
        try:
            with open('tasks.json', 'r+') as file:
                tasks = file.readlines()
                file.seek(0)
                for task in tasks:
                    task_data = json.loads(task)
                    if task_data['description'] != task_to_remove:
                        file.write(json.dumps(task_data) + '\n')
                file.truncate()
        except FileNotFoundError:
            pass

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks = file.readlines()
                for task in tasks:
                    task_data = json.loads(task)
                    self.main_text.insert(END, task_data['description'])
        except FileNotFoundError:
            pass

def main():
    root = Tk()
    ui = Todo(root)
    root.mainloop()

if __name__ == "__main__":
    main()
