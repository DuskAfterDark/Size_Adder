import os
import tkinter as tk
from tkinter import filedialog, messagebox
import mimetypes
from itertools import cycle

DEFAULT_BG = "white"
DARK_BG = "#2c2c2c"
DEFAULT_FG = "black"
DARK_FG = "white"
HIGHLIGHT_COLORS = ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#0000ff", "#4b0082", "#8f00ff"]


RAINBOW_SPEED = 150
RAINBOW_THICKNESS = 2


def toggle_mode():
    if mode_var.get() == "Dark Mode":
        app.configure(bg=DARK_BG)
        for widget in app.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.OptionMenu)):
                widget.configure(bg=DARK_BG, fg=DARK_FG)
    else:
        app.configure(bg=DEFAULT_BG)
        for widget in app.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.OptionMenu)):
                widget.configure(bg=DEFAULT_BG, fg=DEFAULT_FG)

def apply_glowing_rainbow_border(widget):
    colors = cycle(HIGHLIGHT_COLORS)

    def change_color():
        color = next(colors)
        widget.config(highlightbackground=color, highlightcolor=color, highlightthickness=RAINBOW_THICKNESS)
        widget.after(RAINBOW_SPEED, change_color)

    change_color()

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
        file_type, _ = mimetypes.guess_type(file_path)
        if file_type:
            file_type_label.config(text=f"Detected File Type: {file_type}")
            if "application" in file_type:
                apply_glowing_rainbow_border(file_entry)
        else:
            file_type_label.config(text="Detected File Type: Unknown")

def add_size():
    try:
        file_path = file_entry.get()
        size_value = float(size_entry.get())
        unit = unit_var.get()

        if not os.path.isfile(file_path):
            messagebox.showerror("Error", "Selected file does not exist.")
            return

        if unit == "MB":
            additional_bytes = int(size_value * 1024 * 1024)
        elif unit == "GB":
            additional_bytes = int(size_value * 1024 * 1024 * 1024)
        else:
            messagebox.showerror("Error", "Invalid unit selected.")
            return

        with open(file_path, 'ab') as file:
            file.write(b'\0' * additional_bytes)

        messagebox.showinfo("Success", f"{size_value} {unit} added to the file.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid size.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


app = tk.Tk()
app.title("Sizer Adder")
app.geometry("800x600")
app.resizable(True, True)
app.configure(bg=DEFAULT_BG)

mode_var = tk.StringVar(value="Light Mode")
mode_toggle = tk.OptionMenu(app, mode_var, "Light Mode", "Dark Mode", command=lambda _: toggle_mode())
mode_toggle.grid(row=0, column=2, padx=10, pady=10)
mode_toggle.configure(bg="lightgray", fg="black")

file_label = tk.Label(app, text="Select File:")
file_label.grid(row=1, column=0, padx=10, pady=10)

file_entry = tk.Entry(app, width=50, highlightthickness=1)
file_entry.grid(row=1, column=1, padx=10, pady=10)

browse_button = tk.Button(app, text="Browse", command=browse_file)
browse_button.grid(row=1, column=2, padx=10, pady=10)

file_type_label = tk.Label(app, text="Detected File Type:")
file_type_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)


size_label = tk.Label(app, text="Additional Size:")
size_label.grid(row=3, column=0, padx=10, pady=10)

size_entry = tk.Entry(app, width=10, highlightthickness=1)
size_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

unit_var = tk.StringVar(value="MB")
unit_menu = tk.OptionMenu(app, unit_var, "MB", "GB")
unit_menu.grid(row=3, column=2, padx=10, pady=10)
unit_menu.configure(bg="lightgray", fg="black")

add_button = tk.Button(app, text="Add Size", command=add_size)
add_button.grid(row=4, column=0, columnspan=3, pady=20)
add_button.configure(bg="#0078d7", fg="white")

app.mainloop()
