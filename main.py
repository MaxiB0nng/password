import tkinter as tk


def on_click():
    username = username_entry.get()  # Get the username input
    password = password_entry.get()  # Get the password input
    description = description_entry.get()  # Get the description input

    if username.strip() and password.strip() and description.strip():  # Ensure no empty inputs
        global number_password

        # Create a label to show the description (static text)
        description_label = tk.Label(app, text=description)
        description_label.grid(row=number_password, column=0, padx=10, pady=2)

        # Create a label to show the username
        username_label = tk.Label(app, text=username)
        username_label.grid(row=number_password, column=1, padx=10, pady=2)

        # Create a label to show the password (initially masked)
        password_label = tk.Label(app, text="*****")
        password_label.grid(row=number_password, column=2, padx=10, pady=2)

        # Increment row for the next entry
        number_password += 1

        # Add hover functionality for the password
        def show_password(event):
            password_label.config(text=password)  # Show the password on hover

        def hide_password(event):
            password_label.config(text="*****")  # Mask the password when mouse leaves

        # Bind the hover events to the password label
        password_label.bind("<Enter>", show_password)  # On mouse hover
        password_label.bind("<Leave>", hide_password)  # On mouse leave

        # Clear all input fields after submission
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)


# Create the application window
app = tk.Tk()
app.title("Password Manager")

# Keep track of the current row for labels
number_password =8  # Start at row 5 to leave room for input widgets and a blank line

# Set the window size
app.geometry("400x500")  # Adjust size for vertical layout
app.resizable(False, False)

# Widgets
# Description input
description_label = tk.Label(app, text="Description:")
description_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
description_entry = tk.Entry(app, width=30)
description_entry.grid(row=1, column=0, padx=10, pady=5)

# Username input
username_label = tk.Label(app, text="Username:")
username_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
username_entry = tk.Entry(app, width=30)
username_entry.grid(row=3, column=0, padx=10, pady=5)

# Password input
password_label = tk.Label(app, text="Password:")
password_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
password_entry = tk.Entry(app, width=30)
password_entry.grid(row=5, column=0, padx=10, pady=5)

# Submission button
button = tk.Button(app, text="Add Entry", command=on_click)
button.grid(row=6, column=0, padx=10, pady=10)

app.mainloop()
