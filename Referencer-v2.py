import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re
import os
import webbrowser
from urllib.parse import urlparse
from pathlib import Path

# --- Constants ---
MAX_REFERENCES = 500
# Create a dedicated folder in Documents for storing references
REFERENCES_DIR = os.path.join(str(Path.home()), "Documents", "Referencer")
if not os.path.exists(REFERENCES_DIR):
    os.makedirs(REFERENCES_DIR)

STORAGE_FILE = os.path.join(REFERENCES_DIR, "references.json")
APP_TITLE = "OU Harvard Referencing Tool"
VERSION = "2.0"

# --- Theme Colors ---
THEMES = {
    "light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "select_bg": "#0078d7",
        "select_fg": "#ffffff",
        "button_bg": "#f0f0f0",
        "button_fg": "#000000",
        "entry_bg": "#ffffff",
        "entry_fg": "#000000"
    },
    "dark": {
        "bg": "#2d2d2d",
        "fg": "#ffffff",
        "select_bg": "#0078d7",
        "select_fg": "#ffffff",
        "button_bg": "#3d3d3d",
        "button_fg": "#ffffff",
        "entry_bg": "#3d3d3d",
        "entry_fg": "#ffffff"
    }
}

# --- Keyboard Shortcuts ---
SHORTCUTS = {
    "<Control-n>": "add_manual_reference",
    "<Control-f>": "focus_search",
    "<Control-s>": "save_references",
    "<Control-o>": "import_references",
    "<Control-e>": "export_references",
    "<Control-b>": "generate_bibliography",
    "<Control-d>": "delete_reference",
    "<Control-u>": "open_url",
    "<Control-m>": "toggle_theme"
}

class ReferenceApp:
    def __init__(self, master):
        self.master = master
        self.master.title(f"{APP_TITLE} v{VERSION}")
        self.master.geometry("900x700")
        self.references = load_references()
        self.current_folder = "Default"
        self.search_text = ""
        self.current_theme = "light"
        
        # Create menu
        self.create_menu()
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()
        
        # Apply initial theme
        self.apply_theme()
        
        # Main frame
        main_frame = ttk.Frame(master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ... rest of the existing initialization code ...

    def bind_shortcuts(self):
        """Bind keyboard shortcuts to actions"""
        for shortcut, action in SHORTCUTS.items():
            self.master.bind(shortcut, lambda e, a=action: self.handle_shortcut(a))
    
    def handle_shortcut(self, action):
        """Handle keyboard shortcut actions"""
        if action == "add_manual_reference":
            self.add_manual_reference()
        elif action == "focus_search":
            self.search_entry.focus_set()
        elif action == "save_references":
            save_references(self.references)
            messagebox.showinfo("Saved", "References saved successfully.")
        elif action == "import_references":
            self.import_references()
        elif action == "export_references":
            self.export_references(all_folders=False)
        elif action == "generate_bibliography":
            self.generate_bibliography()
        elif action == "delete_reference":
            self.delete_reference()
        elif action == "open_url":
            self.open_url()
        elif action == "toggle_theme":
            self.toggle_theme()
    
    def apply_theme(self):
        """Apply the current theme to all widgets"""
        theme = THEMES[self.current_theme]
        
        # Configure ttk styles
        style = ttk.Style()
        style.configure(".", 
                       background=theme["bg"],
                       foreground=theme["fg"])
        
        style.configure("TButton",
                       background=theme["button_bg"],
                       foreground=theme["button_fg"])
        
        style.configure("TEntry",
                       fieldbackground=theme["entry_bg"],
                       foreground=theme["entry_fg"])
        
        style.configure("TLabel",
                       background=theme["bg"],
                       foreground=theme["fg"])
        
        style.configure("Treeview",
                       background=theme["bg"],
                       foreground=theme["fg"],
                       fieldbackground=theme["bg"])
        
        style.map("Treeview",
                 background=[("selected", theme["select_bg"])],
                 foreground=[("selected", theme["select_fg"])])
        
        # Configure tk widgets
        self.master.configure(bg=theme["bg"])
        
        # Update text widgets
        for widget in [self.full_citation_text, self.intext_citation_text]:
            widget.configure(
                bg=theme["entry_bg"],
                fg=theme["entry_fg"],
                insertbackground=theme["fg"]
            )
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()
        
        # Save theme preference
        try:
            with open(os.path.join(REFERENCES_DIR, "theme.json"), "w") as f:
                json.dump({"theme": self.current_theme}, f)
        except:
            pass

    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import References", command=self.import_references, accelerator="Ctrl+O")
        file_menu.add_command(label="Export All References", command=lambda: self.export_references(all_folders=True), accelerator="Ctrl+E")
        file_menu.add_command(label="Export Current Project", command=lambda: self.export_references(all_folders=False))
        file_menu.add_separator()
        file_menu.add_command(label="Backup References", command=self.backup_references)
        file_menu.add_command(label="Restore from Backup", command=self.restore_references)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Add Manual Reference", command=self.add_manual_reference, accelerator="Ctrl+N")
        edit_menu.add_command(label="Edit Selected Reference", command=self.edit_reference)
        edit_menu.add_command(label="Delete Selected Reference", command=self.delete_reference, accelerator="Ctrl+D")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find Reference...", command=lambda: self.search_entry.focus_set(), accelerator="Ctrl+F")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme, accelerator="Ctrl+M")
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Generate Bibliography", command=self.generate_bibliography, accelerator="Ctrl+B")
        tools_menu.add_command(label="Check for Duplicates", command=self.check_duplicates)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Reference Guide", command=self.show_reference_guide)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_command(label="About", command=self.show_about)
    
    def show_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        dialog = tk.Toplevel(self.master)
        dialog.title("Keyboard Shortcuts")
        dialog.geometry("400x300")
        dialog.transient(self.master)
        
        # Create text widget with shortcuts
        text = tk.Text(dialog, wrap=tk.WORD, padx=10, pady=10)
        text.pack(fill=tk.BOTH, expand=True)
        
        # Add shortcuts
        shortcuts_text = "Keyboard Shortcuts:\n\n"
        for shortcut, action in SHORTCUTS.items():
            # Format shortcut nicely
            shortcut = shortcut.replace("<Control-", "Ctrl+").replace(">", "")
            # Format action nicely
            action = action.replace("_", " ").title()
            shortcuts_text += f"{shortcut}: {action}\n"
        
        text.insert("1.0", shortcuts_text)
        text.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)

# ... rest of the existing code ... 