import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import os
import pandas as pd

# Import Statistics Module
from statistics_module import (
    compute_statistics,
    compute_text_statistics,
    compute_frequency_table
)


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#F4F7FB"

NAVY = "#17324D"

PRIMARY = "#2F6F95"

PRIMARY_DARK = "#245A79"

WHITE = "#FFFFFF"

TEXT = "#243746"

MUTED = "#6B7C8C"

BORDER = "#D9E2EC"

SUCCESS = "#2E8B57"

ERROR = "#C0392B"


# =========================================================
# GLOBAL VARIABLES
# =========================================================

selected_file = ""


# =========================================================
# UPLOAD CSV
# =========================================================
def upload_csv(self):

    file_path = filedialog.askopenfilename(
        title="Select CSV File",

        filetypes=[
            ("CSV Files", "*.csv"),
            ("All Files", "*.*")
        ]
    )

    if file_path:

        self.selected_file = file_path

        filename = os.path.basename(file_path)

        self.file_status_label.configure(
            text=f"✓ {filename}",
            text_color="#16A34A"
        )

        print("Selected file:", file_path)

    else:

        self.file_status_label.configure(
            text="No file selected",
            text_color="#64748B"
        )

def view_comments():

    if selected_file == "":

        messagebox.showwarning(

            "No File",

            "Please upload a CSV file first."
        )

        return

    try:

        df = pd.read_csv(
            selected_file
        )

        # Create new window
        comments_window = tk.Toplevel(
            root
        )

        comments_window.title(
            "Comments"
        )

        comments_window.geometry(
            "800x550"
        )

        comments_window.configure(
            bg=BG_COLOR
        )

        # Header
        header = tk.Label(

            comments_window,

            text="COMMENTS IN DATASET",

            font=(
                "Arial",
                18,
                "bold"
            ),

            bg=BG_COLOR,

            fg=NAVY
        )

        header.pack(
            pady=(25, 5)
        )

        # File name
        filename_label = tk.Label(

            comments_window,

            text=os.path.basename(
                selected_file
            ),

            font=(
                "Arial",
                10,
                "italic"
            ),

            bg=BG_COLOR,

            fg=MUTED
        )

        filename_label.pack(
            pady=(0, 15)
        )

        # Table Frame
        table_frame = tk.Frame(

            comments_window,

            bg=WHITE
        )

        table_frame.pack(

            fill="both",

            expand=True,

            padx=30,

            pady=10
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(

            table_frame,

            orient="vertical"
        )

        scrollbar.pack(

            side="right",

            fill="y"
        )

        # Treeview
        tree = ttk.Treeview(

            table_frame,

            columns=(
                "ID",
                "Comment",
                "Sentiment"
            ),

            show="headings",

            yscrollcommand=scrollbar.set
        )

        tree.heading(
            "ID",
            text="ID"
        )

        tree.heading(
            "Comment",
            text="Comment"
        )

        tree.heading(
            "Sentiment",
            text="Sentiment"
        )

        tree.column(

            "ID",

            width=60,

            anchor="center"
        )

        tree.column(

            "Comment",

            width=500
        )

        tree.column(

            "Sentiment",

            width=120,

            anchor="center"
        )

        tree.pack(

            fill="both",

            expand=True
        )

        scrollbar.config(

            command=tree.yview
        )

        # Insert rows
        for index, row in df.iterrows():

            comment = str(
                row["comment"]
            )

            sentiment = ""

            if "sentiment" in df.columns:

                sentiment = str(
                    row["sentiment"]
                )

            tree.insert(

                "",

                "end",

                values=(

                    index + 1,

                    comment,

                    sentiment
                )
            )

        # Close Button
        close_button = tk.Button(

            comments_window,

            text="Close",

            command=comments_window.destroy,

            bg=PRIMARY,

            fg=WHITE,

            activebackground=PRIMARY_DARK,

            font=(
                "Arial",
                10,
                "bold"
            ),

            relief="flat",

            cursor="hand2",

            padx=25,

            pady=8
        )

        close_button.pack(
            pady=20
        )

    except Exception as e:

        messagebox.showerror(

            "Error",

            f"Unable to display comments.\n\n{e}"
        )


# =========================================================
# ADD COMMENT
# =========================================================

def add_comment():

    if selected_file == "":

        status_label.config(

            text="Please upload a CSV file first",

            fg=ERROR
        )

        return

    comment = comment_box.get(

        "1.0",

        "end-1c"
    ).strip()

    if comment == "":

        status_label.config(

            text="Please enter a comment",

            fg=ERROR
        )

        return

    try:

        df = pd.read_csv(
            selected_file
        )

        # Generate new ID
        new_id = len(df) + 1

        # Create new row
        new_row = pd.DataFrame({

            "ID": [
                new_id
            ],

            "comment": [
                comment
            ],

            "sentiment": [
                ""
            ]
        })

        # Add new row
        df = pd.concat(

            [
                df,
                new_row
            ],

            ignore_index=True
        )

        # Save CSV
        df.to_csv(

            selected_file,

            index=False
        )

        status_label.config(

            text="✓ Comment added successfully",

            fg=SUCCESS
        )

        # Clear comment box
        comment_box.delete(

            "1.0",

            "end"
        )

    except Exception as e:

        messagebox.showerror(

            "Error",

            f"Unable to add comment.\n\n{e}"
        )


# =========================================================
# ANALYZE DATA
# =========================================================

def start_analysis(self):

    if not hasattr(self, "selected_file"):

        self.file_status_label.configure(
            text="Please select a CSV file first",
            text_color="#DC2626"
        )

        return

    print("Starting analysis...")
    print("File:", self.selected_file)

    self.show_frame("Results")

def show_graph():

    result_frame.pack_forget()

    graph_frame.pack(

        fill="both",

        expand=True
    )


def back_to_results():

    graph_frame.pack_forget()

    result_frame.pack(

        fill="both",

        expand=True
    )


def back_to_home():

    result_frame.pack_forget()

    home_frame.pack(

        fill="both",

        expand=True
    )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Social Media Sentiment Analysis"
)

root.geometry(
    "1200x700"
)

root.minsize(
    900,
    600
)

root.configure(
    bg=BG_COLOR
)


# =========================================================
# HOME PAGE
# =========================================================

home_frame = tk.Frame(

    root,

    bg=BG_COLOR
)

home_frame.pack(

    fill="both",

    expand=True
)


# =========================================================
# HEADER
# =========================================================

instruction_label = tk.Label(

    home_frame,

    text="SOCIAL MEDIA SENTIMENT ANALYSIS",

    font=(
        "Arial",
        27,
        "bold"
    ),

    fg=NAVY,

    bg=BG_COLOR
)

instruction_label.pack(

    pady=(45, 5)
)


subtitle_label = tk.Label(

    home_frame,

    text="Analyze public opinion using Machine Learning",

    font=(
        "Arial",
        11,
        "italic"
    ),

    fg=MUTED,

    bg=BG_COLOR
)

subtitle_label.pack(

    pady=(0, 25)
)


# =========================================================
# INPUT CARD
# =========================================================

input_frame = tk.Frame(

    home_frame,

    bg=WHITE,

    highlightbackground=BORDER,

    highlightthickness=1
)

input_frame.pack(

    padx=30,

    pady=10
)


# =========================================================
# CARD TITLE
# =========================================================

card_title = tk.Label(

    input_frame,

    text="DATA INPUT",

    font=(
        "Arial",
        14,
        "bold"
    ),

    fg=NAVY,

    bg=WHITE
)

card_title.pack(

    pady=(25, 15)
)


# =========================================================
# UPLOAD BUTTON
# =========================================================

upload_button = tk.Button(

    input_frame,

    text="Upload CSV File",

    command=upload_csv,

    bg=PRIMARY,

    fg=WHITE,

    activebackground=PRIMARY_DARK,

    activeforeground=WHITE,

    font=(
        "Arial",
        10,
        "bold"
    ),

    relief="flat",

    cursor="hand2",

    padx=25,

    pady=9
)

upload_button.pack()


# =========================================================
# STATUS LABEL
# =========================================================

status_label = tk.Label(

    input_frame,

    text="No file selected",

    font=(
        "Arial",
        10,
        "italic"
    ),

    fg=MUTED,

    bg=WHITE
)

status_label.pack(

    pady=(10, 5)
)


# =========================================================
# VIEW COMMENTS BUTTON
# =========================================================

view_comments_button = tk.Button(

    input_frame,

    text="View Comments",

    command=view_comments,

    state="disabled",

    bg="#E8F0F5",

    fg=PRIMARY,

    font=(
        "Arial",
        10,
        "bold"
    ),

    relief="flat",

    cursor="hand2",

    padx=20,

    pady=7
)

view_comments_button.pack(

    pady=(5, 20)
)


# =========================================================
# SEPARATOR
# =========================================================

separator = ttk.Separator(

    input_frame,

    orient="horizontal"
)

separator.pack(

    fill="x",

    padx=35,

    pady=5
)


# =========================================================
# COMMENT SECTION
# =========================================================

comment_label = tk.Label(

    input_frame,

    text="Enter a Comment",

    font=(
        "Arial",
        11,
        "bold"
    ),

    fg=TEXT,

    bg=WHITE
)

comment_label.pack(

    pady=(20, 8)
)


comment_box = tk.Text(

    input_frame,

    height=4,

    width=60,

    font=(
        "Arial",
        10
    ),

    relief="solid",

    borderwidth=1,

    wrap="word"
)

comment_box.pack(

    padx=35
)


# =========================================================
# ADD COMMENT
# =========================================================

add_comment_button = tk.Button(

    input_frame,

    text="Add Comment",

    command=add_comment,

    bg=WHITE,

    fg=PRIMARY,

    activebackground="#E8F0F5",

    font=(
        "Arial",
        10,
        "bold"
    ),

    relief="solid",

    borderwidth=1,

    cursor="hand2",

    padx=20,

    pady=7
)

add_comment_button.pack(

    pady=(12, 25)
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

analyze_button = tk.Button(

    home_frame,

    text="ANALYZE SENTIMENT",

    command=start_analysis,

    state="disabled",

    bg=NAVY,

    fg=WHITE,

    activebackground="#102638",

    activeforeground=WHITE,

    font=(
        "Arial",
        11,
        "bold"
    ),

    relief="flat",

    cursor="hand2",

    padx=35,

    pady=11
)

analyze_button.pack(

    pady=20
)


# =========================================================
# RESULT PAGE
# =========================================================

result_frame = tk.Frame(

    root,

    bg=BG_COLOR
)


result_title = tk.Label(

    result_frame,

    text="SENTIMENT ANALYSIS RESULTS",

    font=(
        "Arial",
        25,
        "bold"
    ),

    bg=BG_COLOR,

    fg=NAVY
)

result_title.pack(

    pady=(35, 5)
)


result_subtitle = tk.Label(

    result_frame,

    text="Overall Sentiment Analysis",

    font=(
        "Arial",
        12,
        "italic"
    ),

    bg=BG_COLOR,

    fg=MUTED
)

result_subtitle.pack(

    pady=5
)


# =========================================================
# RESULT CARDS
# =========================================================

cards_frame = tk.Frame(

    result_frame,

    bg=BG_COLOR
)

cards_frame.pack(

    pady=25
)


positive_card = tk.Label(

    cards_frame,

    text="POSITIVE\n\n--",

    font=(
        "Arial",
        14,
        "bold"
    ),

    bg=WHITE,

    fg=SUCCESS,

    width=18,

    height=6,

    relief="solid",

    borderwidth=1
)

positive_card.pack(

    side="left",

    padx=15
)


negative_card = tk.Label(

    cards_frame,

    text="NEGATIVE\n\n--",

    font=(
        "Arial",
        14,
        "bold"
    ),

    bg=WHITE,

    fg=ERROR,

    width=18,

    height=6,

    relief="solid",

    borderwidth=1
)

negative_card.pack(

    side="left",

    padx=15
)


neutral_card = tk.Label(

    cards_frame,

    text="NEUTRAL\n\n--",

    font=(
        "Arial",
        14,
        "bold"
    ),

    bg=WHITE,

    fg=PRIMARY,

    width=18,

    height=6,

    relief="solid",

    borderwidth=1
)

neutral_card.pack(

    side="left",

    padx=15
)


# =========================================================
# SUMMARY
# =========================================================

total_label = tk.Label(

    result_frame,

    text="Total Comments: --",

    font=(
        "Arial",
        11,
        "bold"
    ),

    bg=BG_COLOR,

    fg=NAVY
)

total_label.pack(
    pady=3
)


dominant_label = tk.Label(

    result_frame,

    text="Dominant Sentiment: --",

    font=(
        "Arial",
        11
    ),

    bg=BG_COLOR,

    fg=TEXT
)

dominant_label.pack(
    pady=3
)


index_label = tk.Label(

    result_frame,

    text="Sentiment Index: --",

    font=(
        "Arial",
        11
    ),

    bg=BG_COLOR,

    fg=TEXT
)

index_label.pack(
    pady=3
)


# =========================================================
# TEXT STATISTICS
# =========================================================

avg_length_label = tk.Label(

    result_frame,

    text="Average Comment Length: --",

    font=(
        "Arial",
        10
    ),

    bg=BG_COLOR,

    fg=MUTED
)

avg_length_label.pack(
    pady=2
)


median_length_label = tk.Label(

    result_frame,

    text="Median Comment Length: --",

    font=(
        "Arial",
        10
    ),

    bg=BG_COLOR,

    fg=MUTED
)

median_length_label.pack(
    pady=2
)


std_length_label = tk.Label(

    result_frame,

    text="Standard Deviation: --",

    font=(
        "Arial",
        10
    ),

    bg=BG_COLOR,

    fg=MUTED
)

std_length_label.pack(
    pady=2
)


# =========================================================
# FREQUENCY TABLE
# =========================================================

frequency_title = tk.Label(

    result_frame,

    text="Frequency Distribution",

    font=(
        "Arial",
        11,
        "bold"
    ),

    bg=BG_COLOR,

    fg=NAVY
)

frequency_title.pack(

    pady=(10, 5)
)


frequency_tree = ttk.Treeview(

    result_frame,

    columns=(

        "Sentiment",

        "Frequency",

        "Percentage",

        "Cumulative"
    ),

    show="headings",

    height=3
)


frequency_tree.heading(

    "Sentiment",

    text="Sentiment"
)


frequency_tree.heading(

    "Frequency",

    text="Frequency"
)


frequency_tree.heading(

    "Percentage",

    text="Percentage (%)"
)


frequency_tree.heading(

    "Cumulative",

    text="Cumulative Frequency"
)


frequency_tree.pack(

    pady=5
)


# =========================================================
# RESULT BUTTONS
# =========================================================

result_button_frame = tk.Frame(

    result_frame,

    bg=BG_COLOR
)

result_button_frame.pack(

    pady=15
)


view_graph_button = tk.Button(

    result_button_frame,

    text="View Graph",

    command=show_graph,

    bg=PRIMARY,

    fg=WHITE,

    activebackground=PRIMARY_DARK,

    font=(
        "Arial",
        10,
        "bold"
    ),

    relief="flat",

    cursor="hand2",

    padx=25,

    pady=8
)

view_graph_button.pack(

    side="left",

    padx=10
)


back_home_button = tk.Button(

    result_button_frame,

    text="← Back",

    command=back_to_home,

    bg=WHITE,

    fg=PRIMARY,

    font=(
        "Arial",
        10,
        "bold"
    ),

    relief="solid",

    borderwidth=1,

    cursor="hand2",

    padx=25,

    pady=8
)

back_home_button.pack(

    side="left",

    padx=10
)


# =========================================================
# GRAPH PAGE
# =========================================================

graph_frame = tk.Frame(

    root,

    bg=BG_COLOR
)


graph_title = tk.Label(

    graph_frame,

    text="SENTIMENT ANALYSIS DASHBOARD",

    font=(
        "Arial",
        24,
        "bold"
    ),

    bg=BG_COLOR,

    fg=NAVY
)

graph_title.pack(

    pady=50
)


graph_message = tk.Label(

    graph_frame,

    text="Graphs will be displayed here",

    font=(
        "Arial",
        16
    ),

    bg=BG_COLOR,

    fg=MUTED
)

graph_message.pack(

    pady=50
)


back_result_button = tk.Button(

    graph_frame,

    text="← Back to Results",

    command=back_to_results,

    bg=WHITE,

    fg=PRIMARY,

    font=(
        "Arial",
        10,
        "bold"
    ),

    relief="solid",

    borderwidth=1,

    cursor="hand2",

    padx=25,

    pady=8
)

back_result_button.pack(

    pady=20
)


# =========================================================
# START APPLICATION
# =========================================================

root.mainloop()