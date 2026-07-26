import tkinter as tk
from tkinter import filedialog
from tkinter import ttk  # ttk for the grid view
import os
import pandas as pd

def upload_csv():
    # Define the allowed file types (restricting to CSV)
    file_types = [("CSV Files", "*.csv"), ("All Files", "*.*")]
    
    # Open the file dialog and capture the selected file path
    file_path = filedialog.askopenfilename(
        title="Select a CSV File",
        filetypes=file_types,
        initialfile="data.csv"
    )
    
    # Check if the user actually selected a file or cancelled
    if file_path:
        # Extract just the filename for display
        filename = os.path.basename(file_path)
        status_label.config(text=f"Uploaded: {filename}", fg="green")
        
        # Print the full path to the console 
        print(f"Full file path: {file_path}")
            # 1. Read and filter the data
       
    else:
        status_label.config(text="Upload cancelled.", fg="red")


    filename = os.path.basename(file_path)
    df = pd.read_csv("data.csv")
    filtered_df = df[["comment"]]
    print(filtered_df)



# Set up the main application window
root = tk.Tk()
root.title("CSV Uploader")
root.geometry("400x200")

# Add a descriptive label
instruction_label = tk.Label(root, text="Please upload your CSV file below:", font=("Arial", 12))
instruction_label.pack(pady=20)

# Add the Upload Button
# When clicked, it calls the upload_csv function
upload_button = tk.Button(
    root, 
    text="Choose File", 
    command=upload_csv, 
    bg="#4CAF50", 
    fg="white", 
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5
)
upload_button.pack(pady=10)

# Add a status label to show the upload result
status_label = tk.Label(root, text="No file selected", font=("Arial", 10, "italic"), fg="gray")
status_label.pack(pady=15)

# Start the Tkinter event loop
root.mainloop()