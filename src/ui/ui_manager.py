import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import pandas as pd
import os
import sys

# Ensure absolute imports work if script is run directly (fallback)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.core.pipeline import run_analysis_pipeline


class SentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Sentiment Analysis Dashboard")
        self.root.geometry("1300x800")
        self.root.configure(bg="#f4f6f9")
        
        # State
        self.selected_file = None
        self.results = None
        
        # Setup Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#f4f6f9")
        self.style.configure("Card.TFrame", background="white", relief="flat")
        self.style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"), background="#f4f6f9", foreground="#2c3e50")
        self.style.configure("Subtitle.TLabel", font=("Segoe UI", 12), background="#f4f6f9", foreground="#7f8c8d")
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), background="white", foreground="#34495e")
        self.style.configure("Stat.TLabel", font=("Segoe UI", 20, "bold"), background="white", foreground="#2980b9")
        
        # Configure Treeview
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#ecf0f1", foreground="#2c3e50")
        
        # Main Container
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        
        # Initialize Views
        self.frames = {}
        self._init_home_view()
        self._init_loading_view()
        self._init_dashboard_view()
        
        self.show_frame("Home")

    def _init_home_view(self):
        frame = ttk.Frame(self.container)
        self.frames["Home"] = frame
        
        # Title
        ttk.Label(frame, text="Social Media Sentiment Analysis", style="Title.TLabel").pack(pady=(80, 5))
        ttk.Label(frame, text="Upload a dataset to automatically predict sentiments and generate insights.", style="Subtitle.TLabel").pack(pady=(0, 40))
        
        # Action Card
        card = ttk.Frame(frame, style="Card.TFrame", padding=40)
        card.pack(pady=20)
        
        self.file_label = ttk.Label(card, text="No CSV selected", font=("Segoe UI", 10, "italic"), background="white", foreground="#7f8c8d")
        self.file_label.pack(pady=(0, 20))
        
        tk.Button(card, text="Browse CSV File", command=self.upload_csv, 
                  font=("Segoe UI", 11, "bold"), bg="#3498db", fg="white", 
                  relief="flat", padx=20, pady=10, cursor="hand2").pack(pady=(0, 10))
                  
        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=20)
        
        ttk.Label(card, text="Or add a manual comment to the uploaded dataset:", background="white", font=("Segoe UI", 10)).pack(pady=(0, 5))
        self.comment_box = tk.Text(card, height=4, width=50, font=("Segoe UI", 10))
        self.comment_box.pack(pady=(0, 10))
        
        tk.Button(card, text="Add Comment", command=self.add_comment, 
                  font=("Segoe UI", 10, "bold"), bg="#2ecc71", fg="white", 
                  relief="flat", padx=15, pady=5, cursor="hand2").pack()
                  
        # Analyze Button
        self.analyze_btn = tk.Button(frame, text="ANALYZE SENTIMENTS", command=self.start_analysis, 
                  font=("Segoe UI", 14, "bold"), bg="#e67e22", fg="white", 
                  relief="flat", padx=40, pady=12, cursor="hand2")
        self.analyze_btn.pack(pady=40)

    def _init_loading_view(self):
        frame = ttk.Frame(self.container)
        self.frames["Loading"] = frame
        
        ttk.Label(frame, text="Processing Data...", style="Title.TLabel").pack(pady=(200, 10))
        ttk.Label(frame, text="Our ML model is currently analyzing sentiments and generating graphs.", style="Subtitle.TLabel").pack(pady=(0, 30))
        
        self.progress = ttk.Progressbar(frame, mode='indeterminate', length=400)
        self.progress.pack()

    def _init_dashboard_view(self):
        frame = ttk.Frame(self.container)
        self.frames["Dashboard"] = frame
        
        # Header
        header = ttk.Frame(frame)
        header.pack(fill="x", padx=40, pady=20)
        ttk.Label(header, text="Analytics Dashboard", style="Title.TLabel").pack(side="left")
        
        tk.Button(header, text="← Back to Home", command=lambda: self.show_frame("Home"), 
                  font=("Segoe UI", 10, "bold"), bg="#95a5a6", fg="white", 
                  relief="flat", padx=15, pady=5, cursor="hand2").pack(side="right")
                  
        # Content Grid
        self.content = ttk.Frame(frame)
        self.content.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        # We will dynamically populate self.content inside render_dashboard()

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    # ================= CONTROLLERS =================

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")

    def add_comment(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please upload a CSV file first.")
            return
            
        comment = self.comment_box.get("1.0", "end-1c").strip()
        if not comment:
            messagebox.showwarning("Warning", "Comment cannot be empty.")
            return
            
        try:
            df = pd.read_csv(self.selected_file)
            new_id = len(df) + 1
            new_row = pd.DataFrame({"ID": [new_id], "comment": [comment], "sentiment": [""]})
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.selected_file, index=False)
            
            messagebox.showinfo("Success", "Comment appended to the dataset successfully!")
            self.comment_box.delete("1.0", "end")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save comment:\n{e}")

    def start_analysis(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please upload a CSV file before analyzing.")
            return
            
        self.show_frame("Loading")
        self.progress.start(10)
        
        # Run pipeline in background thread
        thread = threading.Thread(target=self._run_pipeline_thread)
        thread.start()

    def _run_pipeline_thread(self):
        try:
            self.results = run_analysis_pipeline(self.selected_file)
            # Switch back to main thread to update UI
            self.root.after(0, self.render_dashboard)
        except Exception as e:
            self.root.after(0, lambda err=e: self._handle_error(err))

    def _handle_error(self, err):
        self.progress.stop()
        self.show_frame("Home")
        messagebox.showerror("Pipeline Error", f"An error occurred during analysis:\n{err}")

    # ================= RENDER DASHBOARD =================

    def render_dashboard(self):
        self.progress.stop()
        
        # Clear existing content in dashboard
        for widget in self.content.winfo_children():
            widget.destroy()
            
        # Top Row: Stats Cards
        stats_frame = ttk.Frame(self.content)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        self._create_stat_card(stats_frame, "POSITIVE", str(self.results["stats"]["positive_count"])).pack(side="left", expand=True, fill="both", padx=(0, 10))
        self._create_stat_card(stats_frame, "NEGATIVE", str(self.results["stats"]["negative_count"])).pack(side="left", expand=True, fill="both", padx=10)
        self._create_stat_card(stats_frame, "NEUTRAL", str(self.results["stats"]["neutral_count"])).pack(side="left", expand=True, fill="both", padx=(10, 0))
        
        # Bottom Row: Data Table
        table_frame = ttk.Frame(self.content, style="Card.TFrame")
        table_frame.pack(fill="both", expand=True)
        ttk.Label(table_frame, text="Processed Data", style="Header.TLabel").pack(anchor="w", padx=20, pady=(20, 10))
        
        # Treeview Scrollbar
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        
        columns = ["Original Comment", "Cleaned Comment", "Sentiment"]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                                 yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
                                 
        scroll_y.config(command=self.tree.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.config(command=self.tree.xview)
        scroll_x.pack(side="bottom", fill="x")
        
        self.tree.heading(columns[0], text=columns[0])
        self.tree.heading(columns[1], text=columns[1])
        self.tree.heading(columns[2], text=columns[2])
        self.tree.column(columns[0], width=500)
        self.tree.column(columns[1], width=400)
        self.tree.column(columns[2], width=150)
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Insert Data
        df = self.results["data"]
        for _, row in df.iterrows():
            c1 = str(row["comment"])
            c2 = str(row["cleaned_comment"])
            s = str(row["sentiment"])
            self.tree.insert("", "end", values=(c1, c2, s))
            
        self.show_frame("Dashboard")

    def _create_stat_card(self, parent, title, value):
        card = ttk.Frame(parent, style="Card.TFrame")
        ttk.Label(card, text=title, style="Header.TLabel").pack(pady=(15, 5))
        ttk.Label(card, text=value, style="Stat.TLabel").pack(pady=(0, 15))
        return card

if __name__ == "__main__":
    root = tk.Tk()
    app = SentimentApp(root)
    root.mainloop()
