import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import os

class Student:
    def __init__(self, name, age, major):
        self.name = name
        self.age = age
        self.major = major

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")  # Set a fixed window size
        self.root.configure(bg="#eaeaea")  # Background color

        # Create database and table
        self.create_database()

        # Font for all components
        self.font = ("Cambria", 12)

        # Create and place labels and entry fields within a frame for better organization
        frame = tk.Frame(root, bg="#eaeaea")
        frame.pack(pady=20)

        tk.Label(frame, text="Name:", font=self.font, bg="#eaeaea").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = tk.Entry(frame, font=self.font, width=30, bd=2)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Age:", font=self.font, bg="#eaeaea").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.age_entry = tk.Entry(frame, font=self.font, width=30, bd=2)
        self.age_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Major:", font=self.font, bg="#eaeaea").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.major_entry = tk.Entry(frame, font=self.font, width=30, bd=2)
        self.major_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons with updated style
        button_frame = tk.Frame(root, bg="#eaeaea")
        button_frame.pack(pady=20)

        self.add_button = ttk.Button(button_frame, text="Add Student", command=self.add_student, width=20)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.delete_button = ttk.Button(button_frame, text="Delete Student", command=self.open_delete_window, width=20)
        self.delete_button.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = ttk.Button(button_frame, text="Search by ID", command=self.open_search_window, width=20)
        self.search_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.display_button = ttk.Button(button_frame, text="Display Students", command=self.display_students, width=20)
        self.display_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Create a frame for the text area and scrollbar for the display
        display_frame = tk.Frame(root, bg="#eaeaea")
        display_frame.pack(pady=20)

        # Create a text area to display the list of students with a scrollbar
        self.text_area = tk.Text(display_frame, height=15, width=60, font=self.font, wrap="word", bg="#f9f9f9", fg="black", bd=2)
        self.text_area.grid(row=0, column=0, padx=10, pady=5)

        # Add scrollbar to the text area
        self.scrollbar = tk.Scrollbar(display_frame, command=self.text_area.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns", padx=5, pady=5)
        self.text_area.config(yscrollcommand=self.scrollbar.set)

    def create_database(self):
        # Remove the existing database file if it exists (for testing purposes)
        if os.path.exists("students.db"):
            os.remove("students.db")

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS STUDENTS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL,
                AGE INTEGER NOT NULL,
                MAJOR TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def add_student(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        major = self.major_entry.get()

        if name and age.isdigit() and major:
            try:
                conn = sqlite3.connect("students.db")
                cursor = conn.cursor()
                cursor.execute('INSERT INTO STUDENTS (NAME, AGE, MAJOR) VALUES (?, ?, ?)', (name, int(age), major))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Student added successfully!")
                self.name_entry.delete(0, tk.END)
                self.age_entry.delete(0, tk.END)
                self.major_entry.delete(0, tk.END)
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Please enter valid information.")

    def open_delete_window(self):
        # Create a new top-level window (popup) for student ID input
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Student")
        delete_window.geometry("400x200")
        delete_window.configure(bg="#eaeaea")

        tk.Label(delete_window, text="Enter Student ID to Delete:", font=self.font, bg="#eaeaea").pack(pady=10)

        delete_id_entry = tk.Entry(delete_window, font=self.font, width=30, bd=2)
        delete_id_entry.pack(pady=10)

        def delete_student():
            student_id = delete_id_entry.get()

            if student_id.isdigit():
                try:
                    conn = sqlite3.connect("students.db")
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM STUDENTS WHERE ID = ?', (int(student_id),))
                    conn.commit()

                    if cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Student deleted successfully!")
                    else:
                        messagebox.showwarning("Not Found", "No student found with that ID.")
                    conn.close()
                    delete_window.destroy()  # Close the popup
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}")
            else:
                messagebox.showerror("Error", "Please enter a valid student ID.")

        # Add Delete button in the popup
        delete_button = ttk.Button(delete_window, text="Delete", command=delete_student, width=15)
        delete_button.pack(pady=20)

    def display_students(self):
        self.text_area.delete(1.0, tk.END)  # Clear previous text
        try:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM STUDENTS')
            fetch = cursor.fetchall()

            if fetch:
                for data in fetch:
                    self.text_area.insert(tk.END, f"ID: {data[0]}, Name: {data[1]}, Age: {data[2]}, Major: {data[3]}\n")
            else:
                self.text_area.insert(tk.END, "No students found.\n")
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def open_search_window(self):
        # Create a new top-level window (popup) for student ID input
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Student by ID")
        search_window.geometry("400x200")
        search_window.configure(bg="#eaeaea")

        tk.Label(search_window, text="Enter Student ID to Search:", font=self.font, bg="#eaeaea").pack(pady=10)

        search_id_entry = tk.Entry(search_window, font=self.font, width=30, bd=2)
        search_id_entry.pack(pady=10)

        def search_student():
            student_id = search_id_entry.get()

            if student_id.isdigit():
                try:
                    conn = sqlite3.connect("students.db")
                    cursor = conn.cursor()
                    cursor.execute('SELECT * FROM STUDENTS WHERE ID = ?', (int(student_id),))
                    data = cursor.fetchone()

                    if data:
                        result_window = tk.Toplevel(search_window)
                        result_window.title("Search Result")
                        result_window.geometry("400x200")
                        result_window.configure(bg="#eaeaea")

                        result_label = tk.Label(result_window, text=f"ID: {data[0]}\nName: {data[1]}\nAge: {data[2]}\nMajor: {data[3]}",
                                                font=self.font, bg="#eaeaea")
                        result_label.pack(pady=20)
                    else:
                        messagebox.showwarning("Not Found", "No student found with that ID.")
                    conn.close()
                    search_window.destroy()  # Close the search window
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}")
            else:
                messagebox.showerror("Error", "Please enter a valid student ID.")

        # Add Search button in the popup
        search_button = ttk.Button(search_window, text="Search", command=search_student, width=15)
        search_button.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()
