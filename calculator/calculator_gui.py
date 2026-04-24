import tkinter as tk

def evaluate_expression(event=None):
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def button_click(char):
    current_text = entry.get()
    if current_text == "Error":
        entry.delete(0, tk.END)
    entry.insert(tk.END, char)

def clear_entry():
    entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x400")
root.resizable(False, False)

# Entry widget for display
entry = tk.Entry(root, width=20, font=("Arial", 24), bd=5, relief=tk.RIDGE, justify=tk.RIGHT)
entry.grid(row=0, column=0, columnspan=4, pady=10)
entry.bind("<Return>", evaluate_expression)

# Define button layout
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
]

# Create and place buttons
for (text, row, col) in buttons:
    if text == '=':
        button = tk.Button(root, text=text, font=("Arial", 18), padx=20, pady=20,
                           command=evaluate_expression, bg="#4CAF50", fg="white")
    else:
        button = tk.Button(root, text=text, font=("Arial", 18), padx=20, pady=20,
                           command=lambda t=text: button_click(t))
    button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

# Clear button
clear_button = tk.Button(root, text="C", font=("Arial", 18), padx=20, pady=20,
                         command=clear_entry, bg="#f44336", fg="white")
clear_button.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=2, pady=2)

# Configure grid to expand buttons
for i in range(5):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Run the application
root.mainloop()
