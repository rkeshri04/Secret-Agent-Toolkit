import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import string

class PasswordGeneratorTool:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, padding=10)
        self.create_widgets()
    
    def create_widgets(self):
        # Configuration section
        config_frame = ttk.LabelFrame(self.frame, text="Password Configuration", padding=10)
        config_frame.pack(fill="both", expand=False, padx=5, pady=5)
        
        # Length setting
        length_frame = ttk.Frame(config_frame)
        length_frame.pack(fill="x", pady=5)
        
        ttk.Label(length_frame, text="Password Length:").pack(side=tk.LEFT, padx=5)
        self.length_var = tk.IntVar(value=12)
        self.length_spinner = ttk.Spinbox(
            length_frame, 
            from_=4, 
            to=64, 
            textvariable=self.length_var, 
            width=5
        )
        self.length_spinner.pack(side=tk.LEFT, padx=5)
        
        # Character options
        char_frame = ttk.Frame(config_frame)
        char_frame.pack(fill="x", pady=5)
        
        self.use_uppercase = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            char_frame, 
            text="Uppercase (A-Z)", 
            variable=self.use_uppercase
        ).pack(side=tk.LEFT, padx=5)
        
        self.use_lowercase = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            char_frame, 
            text="Lowercase (a-z)", 
            variable=self.use_lowercase
        ).pack(side=tk.LEFT, padx=5)
        
        self.use_digits = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            char_frame, 
            text="Digits (0-9)", 
            variable=self.use_digits
        ).pack(side=tk.LEFT, padx=5)
        
        self.use_special = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            char_frame, 
            text="Special Characters", 
            variable=self.use_special
        ).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(config_frame)
        button_frame.pack(fill="x", pady=10)
        
        ttk.Button(
            button_frame, 
            text="Generate Password", 
            command=self.generate_password
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Copy to Clipboard", 
            command=self.copy_to_clipboard
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Save to File", 
            command=self.save_to_file
        ).pack(side=tk.LEFT, padx=5)
        
        # Result section
        result_frame = ttk.LabelFrame(self.frame, text="Generated Password", padding=10)
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            result_frame, 
            textvariable=self.password_var, 
            font=("Courier", 14),
            width=40
        )
        self.password_entry.pack(fill="x", padx=5, pady=10)
        
        # Password history
        history_frame = ttk.LabelFrame(self.frame, text="Password History", padding=10)
        history_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.history_text = tk.Text(history_frame, height=6, width=50)
        self.history_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    def generate_password(self):
        """Generate a random password based on selected criteria"""
        length = self.length_var.get()
        
        # Check that at least one character type is selected
        if not any([
            self.use_uppercase.get(),
            self.use_lowercase.get(),
            self.use_digits.get(),
            self.use_special.get()
        ]):
            messagebox.showwarning("Warning", "Please select at least one character type")
            return
        
        # Define character pool based on selections
        char_pool = ""
        if self.use_uppercase.get():
            char_pool += string.ascii_uppercase
        if self.use_lowercase.get():
            char_pool += string.ascii_lowercase
        if self.use_digits.get():
            char_pool += string.digits
        if self.use_special.get():
            char_pool += string.punctuation
        
        # Generate password
        password = ''.join(random.choice(char_pool) for _ in range(length))
        
        # Update display
        self.password_var.set(password)
        
        # Add to history
        self.history_text.insert("1.0", f"{password}\n")
        
    
    def copy_to_clipboard(self):
        """Copy generated password to clipboard"""
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("Warning", "No password to copy")
            return
        
        self.frame.clipboard_clear()
        self.frame.clipboard_append(password)
    
    def save_to_file(self):
        """Save password to a file"""
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("Warning", "No password to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir="saved_passwords"
        )
        
        if file_path:
            with open(file_path, 'w') as file:
                file.write(password)
