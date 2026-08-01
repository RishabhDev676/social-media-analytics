import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from pathlib import Path
from click import Path
import customtkinter as ctk
import pandas as pd

# Ensure absolute imports work if script is run directly (fallback)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.core.pipeline import run_analysis_pipeline


class SentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Sentiment Analysis Dashboard")
        self.root.geometry("1300x800")
        self.root.minsize(1100, 700)
        try:
            self.root.configure(fg_color="#f4f6f9")
        except Exception:
            try:
                self.root.configure(bg="#f4f6f9")
            except Exception:
                pass

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.selected_file = None
        self.results = None
        self.status_label = None

        self.container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.current_frame_name = None
        self._init_home_view()
        self._init_upload_view()
        self._init_loading_view()
        self._init_results_view()

    def _init_home_view(self):

        # ==========================================
        # HOME FRAME
        # ==========================================

        frame = ctk.CTkFrame(
            self.container,
            fg_color="#FFFFFF",
            corner_radius=0
        )

        self.frames["Home"] = frame

        # ==========================================
        # FIND PROJECT ROOT
        # ==========================================

        current_file = os.path.abspath(__file__)

        ui_dir = os.path.dirname(current_file)
        src_dir = os.path.dirname(ui_dir)
        project_dir = os.path.dirname(src_dir)

        image_path = os.path.join(
            project_dir,
            "data",
            "home_bg.png"
        )

        # ==========================================
        # LOAD IMAGE
        # ==========================================

        bg_image_pil = Image.open(image_path)

        # ==========================================
        # CREATE BACKGROUND IMAGE
        # ==========================================

        bg_image = ctk.CTkImage(
            light_image=bg_image_pil,
            dark_image=bg_image_pil,

            # Use your actual application size
            size=(1600, 950)
        )

        # ==========================================
        # BACKGROUND LABEL
        # ==========================================

        bg_label = ctk.CTkLabel(
            frame,
            text="",
            image=bg_image
        )

        bg_label.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        # Keep image reference
        self.home_bg_image = bg_image

        # ==========================================
        # BUTTON CONTAINER
        # ==========================================

        button_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        button_frame.place(
            relx=0.75,
            rely=0.75,
            anchor="center"
        )

        # ==========================================
        # START ANALYSIS
        # ==========================================

        start_button = ctk.CTkButton(
            button_frame,
            text="START ANALYSIS",

            command=lambda: self.show_frame("Upload"),

            width=240,
            height=50,

            font=(
                "Segoe UI",
                15,
                "bold"
            ),

            fg_color="#2878D0",
            hover_color="#1F5FA8",

            text_color="white",

            corner_radius=12
        )

        start_button.pack(
            pady=(0, 15)
        )

        # ==========================================
        # EXIT
        # ==========================================

        exit_button = ctk.CTkButton(
            button_frame,
            text="EXIT",

            command=self.root.destroy,

            width=240,
            height=45,

            font=(
                "Segoe UI",
                14,
                "bold"
            ),

            fg_color="#FFFFFF",
            hover_color="#E8E8E8",

            text_color="#2878D0",

            border_width=2,
            border_color="#2878D0",

            corner_radius=12
        )

        exit_button.pack()
        self.show_frame("Home")

  
    def _init_upload_view(self):
                # ==================================================
        #                    UPLOAD PAGE
        # ==================================================

        upload_frame = ctk.CTkFrame(
            self.container,
            fg_color="#DDF5F6",
            corner_radius=0
        )

        self.frames["Upload"] = upload_frame


        # ==================================================
        #                    PAGE TITLE
        # ==================================================

        upload_page_title = ctk.CTkLabel(
            upload_frame,
            text="Social Media Sentiment Analysis",
            font=("Segoe UI", 28, "bold"),
            text_color="#172554"
        )

        upload_page_title.pack(
            pady=(35, 5)
        )


        upload_page_subtitle = ctk.CTkLabel(
            upload_frame,
            text="Upload your dataset and analyze public sentiment",
            font=("Segoe UI", 13),
            text_color="#64748B"
        )

        upload_page_subtitle.pack(
            pady=(0, 25)
        )


        # ==================================================
        #                    UPLOAD CARD
        # ==================================================

        input_frame = ctk.CTkFrame(
            upload_frame,
            width=600,
            height=500,
            fg_color="#FFFFFF",
            corner_radius=25
        )

        input_frame.pack(
            pady=10
        )

        input_frame.pack_propagate(False)


        # ==================================================
        #                    UPLOAD ICON
        # ==================================================

        upload_icon = ctk.CTkLabel(
            input_frame,
            text="📁",
            font=("Segoe UI Emoji", 55)
        )

        upload_icon.pack(
            pady=(25, 5)
        )


        # ==================================================
        #                    CARD TITLE
        # ==================================================

        upload_title = ctk.CTkLabel(
            input_frame,
            text="Upload Your Files Here",
            font=("Segoe UI", 21, "bold"),
            text_color="#1E293B"
        )

        upload_title.pack(
            pady=(5, 5)
        )


        # ==================================================
        #                    DESCRIPTION
        # ==================================================

        upload_description = ctk.CTkLabel(
            input_frame,
            text="Upload a CSV file containing comments\n"
                "for sentiment analysis.",
            font=("Segoe UI", 11),
            text_color="#64748B",
            justify="center"
        )

        upload_description.pack(
            pady=(0, 15)
        )


        # ==================================================
        #                    UPLOAD BUTTON
        # ==================================================

        upload_button = ctk.CTkButton(
            input_frame,
            text="Browse Files...",
            command=self.upload_csv,

            width=400,
            height=45,

            font=("Segoe UI", 13, "bold"),

            fg_color="#25A9E0",
            hover_color="#168CC0",

            corner_radius=8
        )

        upload_button.pack(
            pady=8
        )


        # ==================================================
        #                    STATUS LABEL
        # ==================================================

        self.status_label = ctk.CTkLabel(
            input_frame,
            text="No file selected",
            font=("Segoe UI", 11, "italic"),
            text_color="#64748B"
        )

        self.status_label.pack(
            pady=(5, 15)
        )

        back_button = ctk.CTkButton(
            input_frame,
            text="← Back to Home",
            command=self.go_home,
            width=180,
            height=38,
            font=("Segoe UI", 12, "bold"),
            fg_color="#475569",
            hover_color="#334155",
            corner_radius=8
        )
        back_button.pack(
            pady=(0, 10)
        )


        # ==================================================
        #                    COMMENT LABEL
        # ==================================================

        comment_label = ctk.CTkLabel(
            input_frame,
            text="Enter Comment",
            font=("Segoe UI", 12, "bold"),
            text_color="#1E293B"
        )

        comment_label.pack(
            pady=(5, 5)
        )


        # ==================================================
        #                    COMMENT BOX
        # ==================================================

        self.comment_box = ctk.CTkTextbox(
            input_frame,
            width=400,
            height=70,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1"
        )

        self.comment_box.pack(
            pady=5
        )


        # ==================================================
        #                    ADD COMMENT BUTTON
        # ==================================================

        add_comment_button = ctk.CTkButton(
            input_frame,
            text="Add Comment",
            command=self.add_comment,

            width=180,
            height=38,

            font=("Segoe UI", 12, "bold"),

            fg_color="#FFFFFF",
            hover_color="#F1F5F9",

            text_color="#25A9E0",

            border_width=1,
            border_color="#25A9E0",

            corner_radius=8
        )

        add_comment_button.pack(
            pady=8
        )


        # ==================================================
        #                    ANALYZE BUTTON
        # ==================================================

        analyze_button = ctk.CTkButton(
            upload_frame,
            text="ANALYZE",
            command=self.start_analysis,

            width=220,
            height=48,

            font=("Segoe UI", 14, "bold"),

            fg_color="#172554",
            hover_color="#1E3A8A",

            corner_radius=10
        )

        analyze_button.pack(
            pady=20
        )

    def _init_loading_view(self):
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frames["Loading"] = frame

        ctk.CTkLabel(frame, text="Processing Data...", font=("Segoe UI", 24, "bold"), text_color="#2c3e50").pack(pady=(180, 10))
        ctk.CTkLabel(frame, text="The model is running analysis and preparing your results page.", font=("Segoe UI", 12), text_color="#7f8c8d").pack(pady=(0, 30))

        self.progress = ttk.Progressbar(frame, mode="indeterminate", length=400)
        self.progress.pack()

    def _init_results_view(self):
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frames["Results"] = frame

        dashboard_outer = ctk.CTkFrame(frame, fg_color="transparent")
        dashboard_outer.pack(fill="both", expand=True, padx=20, pady=20)

        dashboard_card = ctk.CTkFrame(dashboard_outer, corner_radius=24, fg_color="#FFFFFF", border_width=1, border_color="#D1D5DB")
        dashboard_card.pack(fill="x", padx=80, pady=10)

        header = ctk.CTkFrame(dashboard_card, fg_color="transparent")
        header.pack(fill="x", pady=(20, 10), padx=24)
        ctk.CTkLabel(header, text="Analysis Dashboard", font=("Segoe UI", 26, "bold"), text_color="#1F2937").pack(side="left")
        ctk.CTkButton(header, text="← Upload Again", command=lambda: self.show_frame("Upload"),
                      font=("Segoe UI", 12, "bold"), fg_color="#475569", hover_color="#334155",
                      corner_radius=14, height=44, width=180).pack(side="right")

        buttons_frame = ctk.CTkFrame(dashboard_card, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=24, pady=(0, 22))
        ctk.CTkButton(buttons_frame, text="Show Plots", command=self.show_plots,
                      font=("Segoe UI", 14, "bold"), fg_color="#2563EB", hover_color="#1D4ED8",
                      corner_radius=16, height=48).pack(side="left", expand=True, fill="x", padx=(0, 12))
        ctk.CTkButton(buttons_frame, text="Show Report", command=self.show_report,
                      font=("Segoe UI", 14, "bold"), fg_color="#10B981", hover_color="#059669",
                      corner_radius=16, height=48).pack(side="left", expand=True, fill="x", padx=(0, 12))
        ctk.CTkButton(buttons_frame, text="View Data", command=self.show_data_table,
                      font=("Segoe UI", 14, "bold"), fg_color="#7C3AED", hover_color="#5B21B6",
                      corner_radius=16, height=48).pack(side="left", expand=True, fill="x")

        self.results_content = ctk.CTkFrame(dashboard_card, corner_radius=20, fg_color="#F8FAFC")
        self.results_content.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    def show_frame(self, name):
        if name not in self.frames:
            return
        if self.current_frame_name == name:
            return

        for frame_name, frame in self.frames.items():
            if frame_name == name:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

        self.current_frame_name = name

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.selected_file = file_path
            if self.status_label is not None:
                self.status_label.configure(
                    text=f"Selected: {os.path.basename(file_path)}",
                    text_color="#16A34A"
                )
        else:
            self.selected_file = None
            if self.status_label is not None:
                self.status_label.configure(
                    text="No file selected",
                    text_color="#64748B"
                )

    def go_home(self):
        self.show_frame("Home")

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
            if "comment" not in df.columns:
                raise ValueError("The selected file must contain a 'comment' column.")

            new_id = len(df) + 1
            if "ID" in df.columns:
                new_id = int(df["ID"].dropna().max()) + 1 if not df.empty else 1

            new_row = pd.DataFrame({"ID": [new_id], "comment": [comment], "sentiment": [""]})
            if "ID" not in df.columns:
                df = df.reset_index().rename(columns={"index": "ID"})
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.selected_file, index=False)
            self.comment_box.delete("1.0", "end")
            messagebox.showinfo("Success", "Comment appended to the dataset successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save comment:\n{e}")

    def start_analysis(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please upload a CSV file before analyzing.")
            return

        self.show_frame("Loading")
        self.progress.start(10)
        thread = threading.Thread(target=self._run_pipeline_thread, daemon=True)
        thread.start()

    def _run_pipeline_thread(self):
        try:
            self.results = run_analysis_pipeline(self.selected_file)
            self.root.after(0, self.render_results)
        except Exception as e:
            self.root.after(0, lambda err=e: self._handle_error(err))

    def _handle_error(self, err):
        self.progress.stop()
        self.show_frame("Upload")
        messagebox.showerror("Pipeline Error", f"An error occurred during analysis:\n{err}")

    def render_results(self):
        self.progress.stop()

        for widget in self.results_content.winfo_children():
            widget.destroy()

        stats = self.results["stats"]
        card_row = ctk.CTkFrame(self.results_content, fg_color="transparent")
        card_row.pack(fill="x", pady=(0, 20), padx=10)

        self._create_stat_card(card_row, "Positive", str(stats["positive_count"]), "😊", "Positive statements with favorable sentiment.").pack(side="left", expand=True, fill="both", padx=(0, 10))
        self._create_stat_card(card_row, "Neutral", str(stats["neutral_count"]), "😐", "Neutral statements with balanced sentiment.").pack(side="left", expand=True, fill="both", padx=10)
        self._create_stat_card(card_row, "Negative", str(stats["negative_count"]), "☹️", "Negative statements with critical sentiment.").pack(side="left", expand=True, fill="both", padx=(10, 0))

        info_frame = ctk.CTkFrame(self.results_content, corner_radius=20, fg_color="#FFFFFF", border_width=1, border_color="#E5E7EB")
        info_frame.pack(fill="x", pady=(0, 10), padx=10)
        ctk.CTkLabel(info_frame, text=f"Total Comments: {stats['total']}", font=("Segoe UI", 14, "bold"), text_color="#134E4A").pack(anchor="w", padx=22, pady=(18, 5))
        ctk.CTkLabel(info_frame, text=f"Dominant Sentiment: {stats['dominant_sentiment']}", font=("Segoe UI", 14, "bold"), text_color="#134E4A").pack(anchor="w", padx=22, pady=(0, 18))

        self.show_frame("Results")

    def _create_stat_card(self, parent, title, value, emoji, description):
        card = ctk.CTkFrame(parent, corner_radius=20, fg_color="#FFFFFF", border_width=1, border_color="#E5E7EB", width=320, height=320)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=emoji, font=("Segoe UI Emoji", 58), text_color="#111827").pack(pady=(18, 10))
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 16, "bold"), text_color="#111827").pack(pady=(0, 8))
        ctk.CTkLabel(card, text=value, font=("Segoe UI", 34, "bold"), text_color="#2563EB").pack(pady=(0, 12))
        ctk.CTkLabel(card, text=description, font=("Segoe UI", 12), text_color="#6B7280", wraplength=260, justify="center").pack(padx=18, pady=(0, 18))
        return card

    def show_plots(self):
        if self.results is None:
            messagebox.showwarning("No Results", "Run analysis first to view plots.")
            return

        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import numpy as np

            plot_window = ctk.CTkToplevel(self.root)
            plot_window.title("Sentiment Plots")
            plot_window.geometry("1200x900")

            def _close_plots():
                try:
                    plot_window.destroy()
                except Exception:
                    pass
                self.show_frame("Results")

            # Back button to return to Results
            back_btn = ctk.CTkButton(plot_window, text="← Back", command=_close_plots, width=100, height=36, fg_color="#475569", hover_color="#334155", font=("Segoe UI", 11, "bold"))
            back_btn.pack(anchor="nw", padx=12, pady=12)

            fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=100)

            # --- Sentiment distribution (bar) ---
            sentiment_counts = self.results.get("stats", {})
            labels = ["Positive", "Negative", "Neutral"]
            values = [sentiment_counts.get("positive_count", 0), sentiment_counts.get("negative_count", 0), sentiment_counts.get("neutral_count", 0)]
            axes[0, 0].bar(labels, values, color=["#10B981", "#EF4444", "#F59E0B"])
            axes[0, 0].set_title("Sentiment Distribution", fontsize=14)
            axes[0, 0].set_ylabel("Count", fontsize=12)
            axes[0, 0].tick_params(axis="both", labelsize=10)

            # --- Cumulative sentiment time-series (3 lines) ---
            df = self.results.get("data")
            if df is not None and "sentiment" in df.columns:
                idx = np.arange(len(df))
                pos = (df["sentiment"] == "Positive").cumsum()
                neg = (df["sentiment"] == "Negative").cumsum()
                neu = (df["sentiment"] == "Neutral").cumsum()
                axes[0, 1].plot(idx, pos, label="Positive", color="#10B981", linewidth=2)
                axes[0, 1].plot(idx, neg, label="Negative", color="#EF4444", linewidth=2)
                axes[0, 1].plot(idx, neu, label="Neutral", color="#F59E0B", linewidth=2)
                axes[0, 1].set_title("Cumulative Sentiments Over Records", fontsize=14)
                axes[0, 1].set_xlabel("Record Index", fontsize=11)
                axes[0, 1].set_ylabel("Cumulative Count", fontsize=11)
                axes[0, 1].legend()
            else:
                # Fallback: brief summary line
                axes[0, 1].plot([0, 1, 2], values, marker="o")
                axes[0, 1].set_title("Sentiment Trend (summary)", fontsize=14)

            # --- Character length summary (Avg, Median, Max, Min) ---
            text_col = None
            if df is not None:
                if "cleaned_comment" in df.columns:
                    text_col = "cleaned_comment"
                elif "comment" in df.columns:
                    text_col = "comment"

            if text_col and df is not None:
                lengths = df[text_col].dropna().astype(str).map(len)
                if not lengths.empty:
                    avg_len = float(lengths.mean())
                    med_len = float(lengths.median())
                    max_len = int(lengths.max())
                    min_len = int(lengths.min())
                    labels_l = ["Average", "Median", "Max", "Min"]
                    vals_l = [avg_len, med_len, max_len, min_len]
                    bars = axes[1, 0].bar(labels_l, vals_l, color=["#3B82F6", "#6EE7B7", "#F97316", "#A78BFA"])
                    axes[1, 0].set_title("Text Length Summary", fontsize=14)
                    axes[1, 0].set_ylabel("Characters", fontsize=12)
                    axes[1, 0].tick_params(axis="x", labelsize=11)
                else:
                    axes[1, 0].text(0.5, 0.5, "No text data", ha="center", va="center")
            else:
                axes[1, 0].text(0.5, 0.5, "No text data", ha="center", va="center")

            # --- Sentiment share (pie) ---
            pct = [sentiment_counts.get("positive_pct"), sentiment_counts.get("negative_pct"), sentiment_counts.get("neutral_pct")]
            if None in pct:
                total = sum(values) if sum(values) > 0 else 1
                pct = [v / total * 100 for v in values]
            axes[1, 1].pie(pct, labels=labels, autopct='%1.1f%%', colors=["#10B981", "#EF4444", "#F59E0B"], textprops={"fontsize": 11})
            axes[1, 1].set_title("Sentiment Share", fontsize=14)

            plt.tight_layout()
            fig.subplots_adjust(hspace=0.35, wspace=0.3)
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Plot Error", f"Unable to create plots:\n{e}")

    def show_report(self):
        if self.results is None:
            messagebox.showwarning("No Results", "Run analysis first to view the report.")
            return

        report_window = ctk.CTkToplevel(self.root)
        report_window.title("Analysis Report")
        report_window.geometry("1000x700")

        def _close_report():
            try:
                report_window.destroy()
            except Exception:
                pass
            self.show_frame("Results")

        # Back button for report window
        back_btn_report = ctk.CTkButton(report_window, text="← Back", command=_close_report, width=100, height=36, fg_color="#475569", hover_color="#334155", font=("Segoe UI", 11, "bold"))
        back_btn_report.pack(anchor="nw", padx=12, pady=12)

        # Layout: left = rich text, right = charts
        container = ctk.CTkFrame(report_window, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=12, pady=12)

        left = ctk.CTkFrame(container, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right = ctk.CTkFrame(container, width=360, fg_color="transparent")
        right.pack(side="right", fill="y")

        # Text area with scrollbar
        text_frame = tk.Frame(left)
        text_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text_box = tk.Text(text_frame, wrap="word", padx=18, pady=12, font=("Segoe UI", 11), yscrollcommand=scrollbar.set)
        text_box.pack(fill="both", expand=True)
        scrollbar.config(command=text_box.yview)

        # Define text tags for styling
        text_box.tag_configure("h1", font=("Segoe UI", 18, "bold"), spacing3=6)
        text_box.tag_configure("h2", font=("Segoe UI", 14, "bold"), spacing3=4)
        text_box.tag_configure("bold", font=("Segoe UI", 11, "bold"))
        text_box.tag_configure("mono", font=("Consolas", 10))

        # Build structured report content
        stats = self.results.get("stats", {})
        text_stats = self.results.get("text_stats", {})
        freq_table = self.results.get("freq_table")

        # Header
        text_box.insert("end", "Social Media Sentiment Analysis Report\n", "h1")
        text_box.insert("end", "\n")

        # Summary
        text_box.insert("end", "Summary\n", "h2")
        text_box.insert("end", f"Total comments: ")
        text_box.insert("end", f"{stats.get('total', 0)}\n", "bold")
        text_box.insert("end", f"Dominant sentiment: ")
        text_box.insert("end", f"{stats.get('dominant_sentiment', 'N/A')}\n\n", "bold")

        # Sentiment breakdown
        text_box.insert("end", "Sentiment Breakdown\n", "h2")
        text_box.insert("end", f"Positive: {stats.get('positive_count', 0)} ({stats.get('positive_pct', 0)}%)\n")
        text_box.insert("end", f"Negative: {stats.get('negative_count', 0)} ({stats.get('negative_pct', 0)}%)\n")
        text_box.insert("end", f"Neutral: {stats.get('neutral_count', 0)} ({stats.get('neutral_pct', 0)}%)\n\n")

        # Character length summary
        text_box.insert("end", "Character Length Analysis\n", "h2")
        avg_len = text_stats.get('avg_length') if text_stats else None
        med_len = text_stats.get('median_length') if text_stats else None
        max_len = text_stats.get('max_length') if text_stats else None
        min_len = text_stats.get('min_length') if text_stats else None
        text_box.insert("end", f"Average length: ")
        text_box.insert("end", f"{avg_len}\n" if avg_len is not None else "N/A\n", "bold")
        text_box.insert("end", f"Median length: ")
        text_box.insert("end", f"{med_len}\n" if med_len is not None else "N/A\n", "bold")
        text_box.insert("end", f"Max length: ")
        text_box.insert("end", f"{max_len}\n" if max_len is not None else "N/A\n", "bold")
        text_box.insert("end", f"Min length: ")
        text_box.insert("end", f"{min_len}\n\n" if min_len is not None else "N/A\n\n", "bold")

        # Top repeated words
        text_box.insert("end", "Top Repeated Words\n", "h2")
        if freq_table is not None:
            try:
                # freq_table expected to be pandas DataFrame with 'Sentiment' or word frequencies
                # If it contains word counts, show top entries; otherwise, use constructed freq from data
                if 'Word' in freq_table.columns and 'Frequency' in freq_table.columns:
                    top_words = list(freq_table[['Word', 'Frequency']].head(10).itertuples(index=False, name=None))
                else:
                    # Build from data if freq_table isn't word-based
                    df = self.results.get('data')
                    if df is not None:
                        from collections import Counter
                        words = []
                        text_col = 'cleaned_comment' if 'cleaned_comment' in df.columns else ('comment' if 'comment' in df.columns else None)
                        if text_col:
                            for t in df[text_col].dropna().astype(str):
                                words += [w.lower().strip(".,!?:;\"'()[]()") for w in t.split()]
                        counter = Counter(words)
                        top_words = counter.most_common(10)
                    else:
                        top_words = []
                if top_words:
                    for w, c in top_words:
                        text_box.insert('end', f"{w}: ")
                        text_box.insert('end', f"{c}\n", 'bold')
                else:
                    text_box.insert('end', "No frequent words found.\n")
            except Exception:
                text_box.insert('end', "No frequent words found.\n")
        else:
            text_box.insert('end', "No frequency table available.\n")

        # Footer / notes
        text_box.insert("end", "\nNotes\n", "h2")
        text_box.insert("end", "This report summarizes sentiment counts and character-length statistics for the provided dataset.\n")

        text_box.configure(state="disabled")

        # Right side: small charts for text-length and top words
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4, 6), dpi=100)

            # Character length bar (avg/median/max/min)
            if avg_len is not None:
                labels_l = ["Avg", "Median", "Max", "Min"]
                vals_l = [avg_len or 0, med_len or 0, max_len or 0, min_len or 0]
                ax1.bar(labels_l, vals_l, color=["#3B82F6", "#6EE7B7", "#F97316", "#A78BFA"])
                ax1.set_title("Text Lengths")
            else:
                ax1.text(0.5, 0.5, "No length data", ha="center", va="center")

            # Top words horizontal bar
            words = []
            counts = []
            if freq_table is not None:
                try:
                    if 'Word' in freq_table.columns and 'Frequency' in freq_table.columns:
                        sub = freq_table[['Word', 'Frequency']].head(6)
                        words = list(sub['Word'])
                        counts = list(sub['Frequency'])
                except Exception:
                    pass
            if not words:
                # Try building from data
                df = self.results.get('data')
                if df is not None:
                    from collections import Counter
                    text_col = 'cleaned_comment' if 'cleaned_comment' in df.columns else ('comment' if 'comment' in df.columns else None)
                    if text_col:
                        all_words = []
                        for t in df[text_col].dropna().astype(str):
                            all_words += [w.lower().strip(".,!?:;\"'()[]()") for w in t.split()]
                        counter = Counter(all_words)
                        top = counter.most_common(6)
                        if top:
                            words, counts = zip(*top)

            if words:
                y_pos = range(len(words))[::-1]
                ax2.barh(list(range(len(words)))[::-1], counts, color="#2563EB")
                ax2.set_yticks(list(range(len(words))))
                ax2.set_yticklabels(list(words)[::-1])
                ax2.set_title("Top Words")
            else:
                ax2.text(0.5, 0.5, "No top words", ha="center", va="center")

            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=right)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception:
            # If plotting fails, show a simple message
            ctk.CTkLabel(right, text="Charts unavailable", font=("Segoe UI", 12)).pack(padx=10, pady=10)

    def show_data_table(self):
        if self.results is None:
            messagebox.showwarning("No Results", "Run analysis first to view data.")
            return
        data_window = ctk.CTkToplevel(self.root)
        data_window.title("Processed Data")
        data_window.geometry("1000x650")

        def _close_data():
            try:
                data_window.destroy()
            except Exception:
                pass
            self.show_frame("Results")

        # Back button and heading
        header_frame = ctk.CTkFrame(data_window, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 4))
        back_btn = ctk.CTkButton(header_frame, text="← Back", command=_close_data, width=100, height=36, fg_color="#475569", hover_color="#334155", font=("Segoe UI", 11, "bold"))
        back_btn.pack(side="left")
        ctk.CTkLabel(header_frame, text="Processed Data", font=("Segoe UI", 18, "bold"), text_color="#1F2937").pack(side="left", padx=12)

        frame = ctk.CTkFrame(data_window, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=10, pady=(4, 10))

        # Style Treeview for larger fonts
        style = ttk.Style()
        try:
            style.configure("Custom.Treeview", font=("Segoe UI", 11), rowheight=28)
            style.configure("Custom.Treeview.Heading", font=("Segoe UI", 13, "bold"))
        except Exception:
            pass

        scroll_y = ttk.Scrollbar(frame, orient="vertical")
        scroll_x = ttk.Scrollbar(frame, orient="horizontal")
        tree = ttk.Treeview(frame, columns=["Comment", "Cleaned Comment", "Sentiment"], show="headings", style="Custom.Treeview",
                            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        tree.heading("Comment", text="Comment")
        tree.heading("Cleaned Comment", text="Cleaned Comment")
        tree.heading("Sentiment", text="Sentiment")
        tree.column("Comment", width=520)
        tree.column("Cleaned Comment", width=420)
        tree.column("Sentiment", width=140)

        for _, row in self.results["data"].iterrows():
            tree.insert("", "end", values=(str(row.get("comment", "")), str(row.get("cleaned_comment", "")), str(row.get("sentiment", ""))))

    def _build_report_text(self):
        stats = self.results["stats"]
        text_stats = self.results["text_stats"]
        freq_table = self.results["freq_table"]
        lines = []
        lines.append("Social Media Sentiment Analysis Report")
        lines.append("=" * 40)
        lines.append(f"Total Comments: {stats['total']}")
        lines.append(f"Positive: {stats['positive_count']} ({stats['positive_pct']}%)")
        lines.append(f"Negative: {stats['negative_count']} ({stats['negative_pct']}%)")
        lines.append(f"Neutral: {stats['neutral_count']} ({stats['neutral_pct']}%)")
        lines.append(f"Dominant Sentiment: {stats['dominant_sentiment']}")
        lines.append(f"Average Comment Length: {text_stats.get('avg_length', 0)}")
        lines.append(f"Median Comment Length: {text_stats.get('median_length', 0)}")
        lines.append("")
        lines.append("Sentiment Frequency Table")
        lines.append("-" * 40)
        for _, row in freq_table.iterrows():
            lines.append(f"{row['Sentiment']}: {row['Frequency']} ({row['Percentage (%)']}%)")
        return "\n".join(lines)


if __name__ == "__main__":
    root = ctk.CTk()
    app = SentimentApp(root)
    root.mainloop()
