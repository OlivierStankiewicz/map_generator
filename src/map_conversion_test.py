import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()

print("Choose a JSON file to convert to h3m")
input_file_path = filedialog.askopenfilename(title="Select a JSON file for conversion", filetypes=[("JSON files", "*.json")])
if not input_file_path:
    print("No file selected. Exiting...")
    exit()
print("Selected file:", input_file_path)

print("Choose a folder to save the h3m file")
output_folder = filedialog.askdirectory(title="Select a folder to save the new file")
if not output_folder:
    print("No folder selected. Exiting...")
    exit()
print("Chosen output folder:", output_folder)

new_filename = input("Enter the new file name (without extension): ").strip()
if not new_filename:
    print("No file name provided. Exiting.")
    exit()
print("Chosen new file name:", new_filename)

new_file_path = os.path.join(output_folder, new_filename, ".h3m")

print("Converting JSON to h3m...")
try:
    os.system(f'h3mtxt.exe {input_file_path} {new_file_path}')
except Exception as e:
    print(f"Failed to convert file: {e}")
print("Conversion completed successfully.")
print(f"New file created at: {new_file_path}.h3m")