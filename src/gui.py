import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import pandas as pd


def upload_csv():
    """Opens a file dialog for the user to select a CSV file and displays it."""

    # Define the allowed file types (restricting to CSV)
    file_types = [("CSV Files", "*.csv"), ("All Files", "*.*")]

    # Open the file dialog and capture the selected file path
    file_path = filedialog.askopenfilename(
        title="Select a CSV File",
        filetypes=file_types
    )

    # Check if the user actually selected a file or cancelled
    if file_path:
        # Extract just the filename for display
        filename = os.path.basename(file_path)
        status_label.config(text=f"Uploaded: {filename}", fg="green")

        # Print the full path to the console
        print(f"Full file path: {file_path}")

        # Read the CSV file using the selected path
        try:
            df = pd.read_csv(file_path)
            print(f"\nDataset loaded successfully!")
            print(f"Total rows: {len(df)}")
            print(f"Columns: {list(df.columns)}")
            print(df.head())
        except Exception as e:
            status_label.config(text=f"Error: {e}", fg="red")
            print(f"Error reading file: {e}")
    else:
        status_label.config(text="Upload cancelled.", fg="red")


# Set up the main application window
root = tk.Tk()
root.title("Social Media Sentiment Analyzer")
root.geometry("500x250")

# Add a descriptive label
instruction_label = tk.Label(
    root,
    text="Social Media Sentiment Analysis",
    font=("Arial", 14, "bold")
)
instruction_label.pack(pady=10)

# Add a sub-label
sub_label = tk.Label(
    root,
    text="Upload your CSV file to analyze sentiments",
    font=("Arial", 10)
)
sub_label.pack(pady=5)

# Add the Upload Button
upload_button = tk.Button(
    root,
    text="Choose CSV File",
    command=upload_csv,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5
)
upload_button.pack(pady=15)

# Add a status label to show the upload result
status_label = tk.Label(
    root,
    text="No file selected",
    font=("Arial", 10, "italic"),
    fg="gray"
)
status_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()