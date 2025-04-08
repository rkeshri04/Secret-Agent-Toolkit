import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class CaesarCipherTool:
    def __init__(self, parent, log_callback):
        self.log_callback = log_callback
        self.frame = ttk.Frame(parent, padding=10)
        self.create_widgets()
    
    def create_widgets(self):
        # Input section
        input_frame = ttk.LabelFrame(self.frame, text="Message", padding=10)
        input_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.message_text = tk.Text(input_frame, height=6, width=50)
        self.message_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Control section
        control_frame = ttk.LabelFrame(self.frame, text="Controls", padding=10)
        control_frame.pack(fill="both", padx=5, pady=5)
        
        # Shift value
        shift_frame = ttk.Frame(control_frame)
        shift_frame.pack(fill="x", pady=5)
        
        ttk.Label(shift_frame, text="Shift value:").pack(side=tk.LEFT, padx=5)
        self.shift_var = tk.IntVar(value=3)
        self.shift_spinner = ttk.Spinbox(
            shift_frame, 
            from_=1, 
            to=25, 
            textvariable=self.shift_var, 
            width=5
        )
        self.shift_spinner.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill="x", pady=10)
        
        ttk.Button(
            button_frame, 
            text="Encrypt", 
            command=self.encrypt_message
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Decrypt", 
            command=self.decrypt_message
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Clear", 
            command=self.clear_text
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Save to File", 
            command=self.save_to_file
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Load from File", 
            command=self.load_from_file
        ).pack(side=tk.LEFT, padx=5)
        
        # Result section
        result_frame = ttk.LabelFrame(self.frame, text="Result", padding=10)
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.result_text = tk.Text(result_frame, height=6, width=50)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    def encrypt_message(self):
        message = self.message_text.get("1.0", "end-1c")
        shift = self.shift_var.get()
        
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to encrypt")
            return
        
        encrypted_message = self._caesar_cipher(message, shift)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", encrypted_message)
        self.log_callback(f"Message encrypted with shift {shift}")
    
    def decrypt_message(self):
        message = self.message_text.get("1.0", "end-1c")
        shift = self.shift_var.get()
        
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to decrypt")
            return
        
        decrypted_message = self._caesar_cipher(message, -shift)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", decrypted_message)
        self.log_callback(f"Message decrypted with shift {shift}")
    
    def _caesar_cipher(self, text, shift):
        """Implement Caesar cipher with the given shift"""
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                # Convert letter to 0-25, apply shift, and convert back
                shifted = (ord(char) - ascii_offset + shift) % 26 + ascii_offset
                result += chr(shifted)
            else:
                result += char
        return result
    
    def clear_text(self):
        self.message_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)
        self.log_callback("Cleared cipher text fields")
    
    def save_to_file(self):
        """Save encrypted/decrypted message to a file"""
        text = self.result_text.get("1.0", "end-1c")
        if not text:
            messagebox.showwarning("Warning", "No result to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir="saved_messages"
        )
        
        if file_path:
            with open(file_path, 'w') as file:
                file.write(text)
            self.log_callback(f"Saved message to {os.path.basename(file_path)}")
    
    def load_from_file(self):
        """Load message from a file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir="saved_messages"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                self.message_text.delete("1.0", tk.END)
                self.message_text.insert("1.0", content)
                self.log_callback(f"Loaded message from {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {str(e)}")
