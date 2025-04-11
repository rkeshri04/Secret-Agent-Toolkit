import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re

class MessageDecoderTool:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, padding=10)
        self.create_widgets()
    
    def create_widgets(self):
        # Top section - input options
        input_frame = ttk.LabelFrame(self.frame, text="Message Input", padding=10)
        input_frame.pack(fill="both", expand=False, padx=5, pady=5)
        
        ttk.Button(
            input_frame,
            text="Load from File",
            command=self.load_from_file
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            input_frame,
            text="Paste from Clipboard",
            command=self.paste_from_clipboard
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            input_frame,
            text="Clear All",
            command=self.clear_all
        ).pack(side=tk.LEFT, padx=5)
        
        # Message display
        message_frame = ttk.LabelFrame(self.frame, text="Encoded Message", padding=10)
        message_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.message_text = tk.Text(message_frame, height=6, width=50)
        self.message_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Decoder options
        decoder_frame = ttk.LabelFrame(self.frame, text="Decoder Options", padding=10)
        decoder_frame.pack(fill="both", expand=False, padx=5, pady=5)
        
        self.decoder_type = tk.StringVar(value="firstletter")
        
        ttk.Radiobutton(
            decoder_frame,
            text="First Letter of Each Line",
            variable=self.decoder_type,
            value="firstletter"
        ).pack(anchor="w", padx=5, pady=2)
        
        ttk.Radiobutton(
            decoder_frame,
            text="Every Nth Character",
            variable=self.decoder_type,
            value="everynth"
        ).pack(anchor="w", padx=5, pady=2)
        
        ttk.Radiobutton(
            decoder_frame,
            text="Reverse Text",
            variable=self.decoder_type,
            value="reverse"
        ).pack(anchor="w", padx=5, pady=2)
        
        ttk.Radiobutton(
            decoder_frame,
            text="Find Hidden Pattern",
            variable=self.decoder_type,
            value="pattern"
        ).pack(anchor="w", padx=5, pady=2)
        
        # N value for "Every Nth Character"
        nth_frame = ttk.Frame(decoder_frame)
        nth_frame.pack(fill="x", pady=5)
        
        ttk.Label(nth_frame, text="N value:").pack(side=tk.LEFT, padx=5)
        self.n_value = tk.IntVar(value=3)
        self.n_spinner = ttk.Spinbox(
            nth_frame, 
            from_=2, 
            to=20, 
            textvariable=self.n_value, 
            width=5
        )
        self.n_spinner.pack(side=tk.LEFT, padx=5)
        
        # Pattern for "Find Hidden Pattern"
        pattern_frame = ttk.Frame(decoder_frame)
        pattern_frame.pack(fill="x", pady=5)
        
        # ttk.Label(pattern_frame, text="Pattern:").pack(side=tk.LEFT, padx=5)
        # self.pattern_var = tk.StringVar(value=r"\b[A-Z][a-z]+\b")
        # self.pattern_entry = ttk.Entry(
        #     pattern_frame,
        #     textvariable=self.pattern_var,
        #     width=30
        # )
        # self.pattern_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        # Decode button
        ttk.Button(
            decoder_frame,
            text="Decode Message",
            command=self.decode_message
        ).pack(pady=10)
        
        # Result section
        result_frame = ttk.LabelFrame(self.frame, text="Decoded Result", padding=10)
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.result_text = tk.Text(result_frame, height=6, width=50)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)
    
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
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {str(e)}")
    
    def paste_from_clipboard(self):
        """Paste from clipboard to message area"""
        try:
            clipboard_content = self.frame.clipboard_get()
            self.message_text.delete("1.0", tk.END)
            self.message_text.insert("1.0", clipboard_content)
        except Exception as e:
            messagebox.showerror("Error", f"Could not paste from clipboard: {str(e)}")
    
    def clear_all(self):
        """Clear all text fields"""
        self.message_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)
    
    def decode_message(self):
        """Decode the message based on selected method"""
        message = self.message_text.get("1.0", "end-1c")
        if not message:
            messagebox.showwarning("Warning", "No message to decode")
            return
        
        decoded = ""
        decoder_type = self.decoder_type.get()
        
        if decoder_type == "firstletter":
            # Get first letter of each line
            lines = message.split('\n')
            decoded = ''.join(line[0] for line in lines if line)
            
        elif decoder_type == "everynth":
            # Get every nth character
            n = self.n_value.get()
            decoded = message[::n]
            
        elif decoder_type == "reverse":
            # Reverse the message
            decoded = message[::-1]
            
        elif decoder_type == "pattern":
            # Find pattern matches
            pattern = self.pattern_var.get()
            try:
                matches = re.findall(pattern, message)
                decoded = ' '.join(matches)
            except re.error as e:
                messagebox.showerror("Error", f"Invalid regex pattern: {str(e)}")
                return
        
        # Update result
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", decoded)
