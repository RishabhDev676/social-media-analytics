import os
import sys
import tkinter as tk

# 1. Setup Environment
# Ensure the root directory of the project is in the Python path
# This prevents "ModuleNotFoundError: No module named 'src'"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Now we can safely import from our src packages
try:
    from src.ui.ui_manager import SentimentApp
except ImportError as e:
    print(f"CRITICAL ERROR: Failed to load application modules.\nDetails: {e}")
    print("\nPlease ensure all dependencies (pandas, scikit-learn, matplotlib) are installed.")
    sys.exit(1)

def main():
    """
    Bootstrapper for the Social Media Sentiment Analysis application.
    Initializes the Tkinter root and launches the Dashboard.
    """
    print("Booting Social Media Sentiment Analysis Dashboard...")
    
    # Initialize UI
    root = tk.Tk()
    
    # Instantiate the application
    app = SentimentApp(root)
    
    # Start the event loop
    root.mainloop()

if __name__ == "__main__":
    main()
