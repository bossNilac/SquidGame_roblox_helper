import tkinter as tk
from tkinter import messagebox
import json

# Path to save key bindings
KEY_BIND_FILE = "res/key_binds.json"
character_keys = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z",  # Lowercase letters
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",  # Numbers
    "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/"  # Non-shift special characters
]


# Key detection callback
def on_key_press(event, entry_field):
    key = event.keysym  # Get the key symbol
    if len(key) > 1:  # Only accept function keys, special keys, or digits
        entry_field.delete(0, tk.END)  # Clear the entry field
        print(key)
        if entry_field.get() == '':
            if key not in character_keys:
                entry_field.insert(0, key)  # Insert the key symbol
                if key == 'BackSpace':
                    entry_field.insert(tk.END, 'e')
    elif key in character_keys:
        entry_field.delete(0, tk.END)
    elif key == entry_field.get() or key in entry_field.get():
        entry_field.delete(0, tk.END)


# Load existing key binds if the file exists
try:
    with open(KEY_BIND_FILE, "r") as file:
        key_binds = json.load(file)
except FileNotFoundError:
    key_binds = {
        "activate_help": "",
        "drawing": "",
        "rope_pulling": "",
        "sound_play": ""
    }


def main():
    # Function to save key bindings to JSON
    def save_key_binds():
        key_binds = {
            "activate_help": entry_activate_all.get(),
            "drawing": entry_drawing.get(),
            "rope_pulling": entry_rope_pulling.get(),
            "sound_play": entry_sound_play.get()
        }

        with open(KEY_BIND_FILE, "w") as file:
            json.dump(key_binds, file, indent=4)
        messagebox.showinfo("Success", "Key bindings saved successfully!")

    # Create the main window
    root = tk.Tk()
    root.title("Set Key Binds")
    root.geometry("400x300")

    # Labels and Entry fields
    lbl_activate_all = tk.Label(root, text="Bind to Activate Helper:")
    lbl_activate_all.pack(pady=5)
    entry_activate_all = tk.Entry(root)
    entry_activate_all.pack(pady=5)
    entry_activate_all.insert(0, key_binds.get("activate_help", ""))
    entry_activate_all.bind("<KeyPress>", lambda event: on_key_press(event, entry_activate_all))

    lbl_drawing = tk.Label(root, text="Bind for Toggle Drawing Help:")
    lbl_drawing.pack(pady=5)
    entry_drawing = tk.Entry(root)
    entry_drawing.pack(pady=5)
    entry_drawing.insert(0, key_binds.get("drawing", ""))
    entry_drawing.bind("<KeyPress>", lambda event: on_key_press(event, entry_drawing))

    lbl_rope_pulling = tk.Label(root, text="Bind for Toggle Rope Pulling Assist:")
    lbl_rope_pulling.pack(pady=5)
    entry_rope_pulling = tk.Entry(root)
    entry_rope_pulling.pack(pady=5)
    entry_rope_pulling.insert(0, key_binds.get("rope_pulling", ""))
    entry_rope_pulling.bind("<KeyPress>", lambda event: on_key_press(event, entry_rope_pulling))

    lbl_sound_play = tk.Label(root, text="Bind for GreenLight Sound Play:")
    lbl_sound_play.pack(pady=5)
    entry_sound_play = tk.Entry(root)
    entry_sound_play.pack(pady=5)
    entry_sound_play.insert(0, key_binds.get("sound_play", ""))
    entry_sound_play.bind("<KeyPress>", lambda event: on_key_press(event, entry_sound_play))

    # Save button
    btn_save = tk.Button(root, text="Save Key Binds", command=save_key_binds)
    btn_save.pack(pady=20)

    # Run the GUI event loop
    root.mainloop()


