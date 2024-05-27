import json
import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from ttkthemes import ThemedTk

def change_framerate_limit(db_path, new_framerate):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)

        # Create a cursor object
        cur = conn.cursor()

        # Execute a SQL query to get the JSON data
        cur.execute("SELECT value FROM LocalStorage WHERE key = 'GameQualitySetting'")
        result = cur.fetchone()
        if result:
            data = json.loads(result[0])

            # Check if the 'KeyCustomFrameRate' key exists in the JSON data
            if 'KeyCustomFrameRate' in data:
                # Change the framerate limit
                data['KeyCustomFrameRate'] = new_framerate

                # Convert the data back to a JSON string
                json_data = json.dumps(data)

                # Execute a SQL query to update the JSON data
                cur.execute("UPDATE LocalStorage SET value = ? WHERE key = 'GameQualitySetting'", (json_data,))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

def select_file_path(entry):
    file_path = filedialog.askopenfilename(initialdir="D:/Wuthering Waves/Wuthering Waves Game/Client/Saved/LocalStorage", filetypes=[('Database Files', '*.db')])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def apply_changes(entry, scale):
    file_path = entry.get()
    fps = scale.get()
    if fps > 120:
        messagebox.showwarning("Warning", "Setting FPS above 120 is usually not necessary! Use with caution.")
    if change_framerate_limit(file_path, fps):
        messagebox.showinfo("Success", "Changes applied successfully!")

def create_window():
    window = ThemedTk(theme="arc")  # Use the "arc" theme
    window.title("FPS Changer Tool")
    window.geometry('650x200')
    window.iconbitmap('icon.ico')  # Add this line

    ttk.Label(window, text="Database File Path:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    file_path_entry = ttk.Entry(window, width=50)
    file_path_entry.grid(row=0, column=1, padx=10, pady=10)

    file_path_entry.insert(0, "D:/Wuthering Waves/Wuthering Waves Game/Client/Saved/LocalStorage/LocalStorage.db")

    select_button = ttk.Button(window, text="Select File", command=lambda: select_file_path(file_path_entry))
    select_button.grid(row=0, column=2, padx=10, pady=10)

    ttk.Label(window, text="FPS:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    fps_value = tk.StringVar()
    fps_scale = ttk.Scale(window, from_=1, to=240, orient=tk.HORIZONTAL, length=400, command=lambda s: fps_value.set('%d' % float(s)))
    fps_scale.grid(row=1, column=1, padx=10, pady=10)

    fps_label = ttk.Label(window, textvariable=fps_value)
    fps_label.grid(row=1, column=2, padx=10, pady=10)

    apply_button = ttk.Button(window, text="Apply", command=lambda: apply_changes(file_path_entry, fps_scale))
    apply_button.grid(row=2, column=1, padx=10, pady=10)

    window.mainloop()

# Usage
create_window()