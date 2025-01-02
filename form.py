import sqlite3
import tkinter as tk
from tkinter import messagebox


def create_table():
    conn = sqlite3.connect('employee_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empdetail (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            FIRST_NAME TEXT,
            LAST_NAME TEXT,
            email TEXT,
            phone_number INTEGER
        );
    ''')
    conn.commit()
    conn.close()


def insert_data():
    FIRST_NAME = entry_name1.get()  
    LAST_NAME = entry_name2.get()
    email = entry_email.get()
    phone_number = entry_phone.get() 

    if FIRST_NAME and LAST_NAME and email and phone_number:
        try:
            conn = sqlite3.connect('employee_data.db')
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM empdetail WHERE email = ?', (email,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Email ID already exists! Please choose a different email.")
                conn.close()
                return

            cursor.execute('SELECT * FROM empdetail WHERE phone_number = ?', (phone_number,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Phone Number already exists! Please choose a different phone number.")
                conn.close()
                return

            cursor.execute('SELECT * FROM empdetail WHERE FIRST_NAME = ? AND LAST_NAME = ?', (FIRST_NAME, LAST_NAME))
            if cursor.fetchone():
                messagebox.showerror("Error", "An employee with the same name already exists!")
                conn.close()
                return

            cursor.execute(''' 
                INSERT INTO empdetail (FIRST_NAME, LAST_NAME, email, phone_number)
                VALUES (?, ?, ?, ?)
            ''', (FIRST_NAME, LAST_NAME, email, phone_number))
            conn.commit()
            messagebox.showinfo("Success", "Data has been added to the database!")
            
            
            entry_name1.delete(0, tk.END)
            entry_name2.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_phone.delete(0, tk.END)
            conn.close()
        
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Error", "Please fill out all fields.")


def update_data(ID):
    def save_update():
        updated_name1 = entry_up_name1.get()
        updated_name2 = entry_up_name2.get()
        updated_email = entry_up_email.get()
        updated_phone = entry_up_phone.get() 

        if updated_name1 and updated_name2 and updated_email and updated_phone:
            try:
                conn = sqlite3.connect('employee_data.db')
                cursor = conn.cursor()

                cursor.execute('SELECT * FROM empdetail WHERE email = ? AND ID != ?', (updated_email, ID))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Email ID already exists! Please choose a different email.")
                    conn.close()
                    return

                cursor.execute('SELECT * FROM empdetail WHERE phone_number = ? AND ID != ?', (updated_phone, ID))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Phone Number already exists! Please choose a different phone number.")
                    conn.close()
                    return

                cursor.execute('SELECT * FROM empdetail WHERE FIRST_NAME = ? AND LAST_NAME = ? AND ID != ?', (updated_name1, updated_name2, ID))
                if cursor.fetchone():
                    messagebox.showerror("Error", "An employee with the same name already exists!")
                    conn.close()
                    return

                cursor.execute('''
                    UPDATE empdetail
                    SET FIRST_NAME = ?, LAST_NAME = ?, email = ?, phone_number = ?
                    WHERE ID = ?
                ''', (updated_name1, updated_name2, updated_email, updated_phone, ID))
                conn.commit()
                messagebox.showinfo("Success", "Data has been updated successfully!")
                conn.close()
                update_window.destroy()

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Please fill out all fields.")

    update_window = tk.Toplevel(root)
    update_window.title("Update Employee Data")

    tk.Label(update_window, text="First Name:").grid(row=1, column=0, padx=10, pady=10)
    entry_up_name1 = tk.Entry(update_window)
    entry_up_name1.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(update_window, text="Last Name:").grid(row=2, column=0, padx=10, pady=10)
    entry_up_name2 = tk.Entry(update_window)
    entry_up_name2.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(update_window, text="Email:").grid(row=3, column=0, padx=10, pady=10)
    entry_up_email = tk.Entry(update_window)
    entry_up_email.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(update_window, text="Phone Number:").grid(row=4, column=0, padx=10, pady=10)
    entry_up_phone = tk.Entry(update_window)
    entry_up_phone.grid(row=4, column=1, padx=10, pady=10)

    save_button = tk.Button(update_window, text="Save Update", command=save_update)
    save_button.grid(row=5, column=0, columnspan=2, pady=20)

    conn = sqlite3.connect('employee_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM empdetail WHERE ID = ?', (ID,))
    record = cursor.fetchone()
    conn.close()

    if record:
        entry_up_name1.insert(0, record[1]) 
        entry_up_name2.insert(0, record[2]) 
        entry_up_email.insert(0, record[3]) 
        entry_up_phone.insert(0, record[4]) 


def delete_data(ID):
    def confirm_delete():
        if ID:
            conn = sqlite3.connect('employee_data.db')
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM empdetail WHERE ID = ?
            ''', (ID,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "The given employee ID has been deleted.")
            delete_window.destroy()

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Employee Data")

    tk.Label(delete_window, text="Are you sure you want to delete this record?").grid(row=0, column=0, padx=10, pady=10)
    
    delete_button = tk.Button(delete_window, text="Yes, Delete", command=confirm_delete)
    delete_button.grid(row=1, column=0, columnspan=2, pady=20)


def view_data():
    conn = sqlite3.connect('employee_data.db') 
    cursor = conn.cursor() 
    cursor.execute('SELECT * FROM empdetail')
    rows = cursor.fetchall()
    conn.close()

    view_window = tk.Toplevel(root)
    view_window.title("View Employee Data")

    tk.Label(view_window, text="ID", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(view_window, text="First Name", font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=5)
    tk.Label(view_window, text="Last Name", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=5)
    tk.Label(view_window, text="Email", font=("Arial", 12)).grid(row=0, column=3, padx=10, pady=5)
    tk.Label(view_window, text="Phone Number", font=("Arial", 12)).grid(row=0, column=4, padx=10, pady=5)

    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            tk.Label(view_window, text=value, font=("Arial", 12)).grid(row=i+1, column=j, padx=10, pady=5)
        
        update_button = tk.Button(view_window, text="Update", command=lambda id=row[0]: update_data(id))
        update_button.grid(row=i+1, column=5, padx=10, pady=5)

        delete_button = tk.Button(view_window, text="Delete", command=lambda id=row[0]: delete_data(id))
        delete_button.grid(row=i+1, column=6, padx=10, pady=5)



root = tk.Tk()
root.title("Employee Data Entry Form")


tk.Label(root, text="First Name:").grid(row=0, column=0, padx=10, pady=10)
entry_name1 = tk.Entry(root)
entry_name1.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Last Name:").grid(row=1, column=0, padx=10, pady=10)
entry_name2 = tk.Entry(root)
entry_name2.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Email:").grid(row=2, column=0, padx=10, pady=10)
entry_email = tk.Entry(root)
entry_email.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Phone Number:").grid(row=3, column=0, padx=10, pady=10)
entry_phone = tk.Entry(root)
entry_phone.grid(row=3, column=1, padx=10, pady=10)

submit_button = tk.Button(root, text="Submit", command=insert_data)
submit_button.grid(row=4, column=0, columnspan=2, pady=20)

view_button = tk.Button(root, text="View Data", command=view_data)
view_button.grid(row=5, column=0, columnspan=2, pady=10)

create_table()

root.mainloop()
