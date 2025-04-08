import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import tool modules
from utils.caesar_cipher import CaesarCipherTool
from utils.password_generator import PasswordGeneratorTool
from utils.message_decoder import MessageDecoderTool

class SecretAgentToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Secret Agent Toolkit")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        # Set icon if available
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        
        self.create_widgets()
        self.log_activity("Application started")
    
    def create_widgets(self):
        # Top header
        header_frame = tk.Frame(self.root, bg="#34495e", pady=10)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame, 
            text="SECRET AGENT TOOLKIT", 
            font=("Arial", 20, "bold"),
            fg="#ecf0f1",
            bg="#34495e"
        ).pack()
        
        # Create notebook for different tools
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Initialize tools and add to notebook
        self.caesar_tool = CaesarCipherTool(self.notebook, self.log_activity)
        self.password_tool = PasswordGeneratorTool(self.notebook, self.log_activity)
        self.decoder_tool = MessageDecoderTool(self.notebook, self.log_activity)
        
        self.notebook.add(self.caesar_tool.frame, text="Caesar Cipher")
        self.notebook.add(self.password_tool.frame, text="Password Generator")
        self.notebook.add(self.decoder_tool.frame, text="Message Decoder")
        
        # Status bar
        self.status_bar = tk.Label(
            self.root, 
            text="Ready", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg="#7f8c8d",
            fg="white"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def log_activity(self, message):
        """Log user activities to a file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Update status bar
        self.status_bar.config(text=message)
        
        # Write to log file
        with open("logs/activity_log.txt", "a") as log_file:
            log_file.write(log_message)

if __name__ == "__main__":
    # Create required directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("saved_messages", exist_ok=True)
    os.makedirs("tools", exist_ok=True)
    
    # Initialize and run the application
    root = tk.Tk()
    app = SecretAgentToolkit(root)
    root.mainloop()
