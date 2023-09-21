#How To Use
#Enter your username (partial or full) and select a ZIP file to search for related lines of text.

import os
import re
import zipfile
import tempfile
import tkinter as tk
from tkinter import filedialog, scrolledtext, simpledialog

# Regular expression to capture the author and text from the JSON content
pattern = r'"author": "(?P<author>.*?)",.*?"text": "(?P<text>.*?)"'

def extract_and_search(zip_path, username):
    # Initialize a dictionary to store the related lines
    related_lines_local = {}

    # Create a temporary directory to extract the ZIP contents
    with tempfile.TemporaryDirectory() as tmpdirname:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdirname)

        # Iterate through each file in the temporary directory
        for file_name in os.listdir(tmpdirname):
            file_path = os.path.join(tmpdirname, file_name)

            # Open the file and read its content
            with open(file_path, 'r', errors='replace') as file:
                content = file.read()
                matches = re.findall(pattern, content)
                for match in matches:
                    author, text = match
                    if username in author:
                        if file_name not in related_lines_local:
                            related_lines_local[file_name] = []
                        related_lines_local[file_name].append(f"{author} - {text}")

    # Filter for unique lines and return the results
    output = []
    for file, lines in related_lines_local.items():
        unique_lines = list(set(lines))
        sorted_unique_lines = sorted(unique_lines)
        output.append(f"In file {file}:")
        output.extend(iter(sorted_unique_lines))
        output.append("\n")
    return "\n".join(output)

def select_zip_file():
    # Ask the user for the username
    username = simpledialog.askstring("Input", "Please enter the username:")
    if not username:
        return

    if file_path := filedialog.askopenfilename(
        title="Select ZIP File", filetypes=[("ZIP files", "*.zip")]
    ):
        results = extract_and_search(file_path, username)
        # Display the results in the text box
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, results)

# Create the main GUI window
root = tk.Tk()
root.title("ZIP Search Tool")
root.geometry("600x400")

# Dark mode colors
bg_color = '#2E2E2E'
fg_color = '#FFFFFF'
btn_color = '#424242'
text_box_color = '#424242'

# Apply dark mode colors
root.configure(bg=bg_color)

# Add a button to select the ZIP file
btn = tk.Button(root, text="Select Username and ZIP File", command=select_zip_file, bg=btn_color, fg=fg_color)
btn.pack(pady=20)

# Add a scrolled text box to display the results
text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, bg=text_box_color, fg=fg_color, insertbackground=fg_color)
text_box.pack(pady=20)

root.mainloop()