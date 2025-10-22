import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
CONFIG_FILE = "config.json"
class DirectorySelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory Selector")
        self.entries = {}

        # number of directory fields (can be dynamic if needed)
        self.num_dirs = 4  

        
        frame = tk.Frame(root)
        frame.pack(padx=10, pady=5, fill='x')
        label = tk.Label(frame, text=f"CSDK directory:")
        label.pack(side='left', padx=5)
        entry = tk.Entry(frame, width=50)
        entry.pack(side='left', padx=5, fill='x', expand=True)
        self.entries["CSDK_directory"]=entry
        button = tk.Button(frame, text="Browse", command=lambda e=entry: self.browse_dir(e))
        button.pack(side='left', padx=5)

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=5, fill='x')
        label = tk.Label(frame, text=f"Source 2 Viewer directory:")
        label.pack(side='left', padx=5)
        entry = tk.Entry(frame, width=50)
        entry.pack(side='left', padx=5, fill='x', expand=True)
        self.entries["Source_2_Viewer_directory"]=entry
        button = tk.Button(frame, text="Browse", command=lambda e=entry: self.browse_dir(e))
        button.pack(side='left', padx=5)

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=5, fill='x')
        label = tk.Label(frame, text=f"Dead Packer directory:")
        label.pack(side='left', padx=5)
        entry = tk.Entry(frame, width=50)
        entry.pack(side='left', padx=5, fill='x', expand=True)
        self.entries["dead_packer_directory"]=entry
        button = tk.Button(frame, text="Browse", command=lambda e=entry: self.browse_dir(e))
        button.pack(side='left', padx=5)

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=5, fill='x')
        label = tk.Label(frame, text=f"Deadlock directory:")
        label.pack(side='left', padx=5)
        entry = tk.Entry(frame, width=50)
        entry.pack(side='left', padx=5, fill='x', expand=True)
        self.entries["Deadlock_directory"]=entry
        button = tk.Button(frame, text="Browse", command=lambda e=entry: self.browse_dir(e))
        button.pack(side='left', padx=5)
        

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        save_button = tk.Button(button_frame, text="Save Config", command=self.save_config)
        save_button.pack(side='left', padx=5)

        start_button = tk.Button(button_frame, text="Start Game", command=self.start_game)
        start_button.pack(side='right', padx=5)


        # Load config on startup if available
        self.load_config()

    def browse_dir(self, entry):
        path = filedialog.askdirectory()
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)


    def save_config(self):
        data = {key: e.get() for key, e in self.entries.items()}
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Saved", f"Configuration saved to {CONFIG_FILE}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")

    def start_game(self):
        os.system(f"cmd /c run.bat")
        root.destroy() 

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return  # nothing to load yet
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
            for entry, path in data.items():
                self.entries[entry].delete(0, tk.END)
                self.entries[entry].insert(0, path)
            print("Config loaded:", data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config: {e}")

    def submit(self):
        paths = [e.get() for e in self.entries]
        print("Selected directories:")
        for p in paths:
            print(p)

if __name__ == "__main__":
    root = tk.Tk()
    app = DirectorySelectorApp(root)
    root.mainloop()
