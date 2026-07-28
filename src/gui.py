import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import pandas as pd


# ================= GLOBAL VARIABLES =================

selected_file = ""


# ================= FUNCTIONS =================

def upload_csv():
    global selected_file #global variable to track csvpath 

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("CSV Files", "*.csv"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        selected_file = file_path

        filename = os.path.basename(selected_file)

        status_label.config(
            text=f"Uploaded: {filename}",
            fg="blue"
        )

        # Read selected CSV
        df = pd.read_csv(selected_file)

        # Display comments in console
        filtered_df = df[["comment"]]

        print(filtered_df)

    else:
        status_label.config(
            text="No file selected",
            fg="gray"
        )


def add_comment():

    if selected_file == "":
        status_label.config(
            text="Please upload a CSV first",
            fg="red"
        )
        return

    comment = comment_box.get("1.0", "end-1c").strip()

    # Check comment
    if comment == "":
        status_label.config(
            text="Please enter a comment",
            fg="red"
        )
        return

    # Read CSV
    df = pd.read_csv(selected_file)

    # Generate new ID
    new_id = len(df) + 1

    # Create new row
    new_row = pd.DataFrame({
        "ID": [new_id],
        "comment": [comment],
        "sentiment": [""]   # Leave blank since it hasn't been predicted yet
    })

    # Add new row
    df = pd.concat([df, new_row], ignore_index=True)

    # Save updated CSV
    df.to_csv(selected_file, index=False)

    status_label.config(
        text="Comment added successfully!",
        fg="green"
    )

    # Clear inputs
    comment_box.delete("1.0", "end")
   


# ================= PAGE NAVIGATION =================

def show_results():

    # Hide home page
    home_frame.pack_forget()

    # Show result page
    result_frame.pack(fill="both", expand=True)


def show_graph():

    # Hide result page
    result_frame.pack_forget()

    # Show graph page
    graph_frame.pack(fill="both", expand=True)


def back_to_results():

    # Hide graph page
    graph_frame.pack_forget()

    # Show result page
    result_frame.pack(fill="both", expand=True)


def back_to_home():

    # Hide result page
    result_frame.pack_forget()

    # Show home page
    home_frame.pack(fill="both", expand=True)


# ================= MAIN WINDOW =================

root = tk.Tk()

root.title("Social Media Sentiment Analysis")

root.geometry("1200x700")

root.configure(bg="#EFF7FF")


# ==================================================
#                    HOME PAGE
# ==================================================

home_frame = tk.Frame(
    root,
    bg="#EFF7FF"
)

home_frame.pack(
    fill="both",
    expand=True
)


# ---------- HEADER ----------

instruction_label = tk.Label(
    home_frame,
    text="SOCIAL MEDIA SENTIMENT ANALYSIS",
    font=("Book Antiqua", 24, "bold"),
    fg="#558CBD",
    bg="#EFF7FF"
)

instruction_label.pack(pady=(40, 5))


subtitle_label = tk.Label(
    home_frame,
    text="Analyze public opinion using Machine Learning",
    font=("Arial", 11, "italic"),
    fg="#666666",
    bg="#EFF7FF"
)

subtitle_label.pack(pady=(0, 30))


# ---------- MAIN INPUT CARD ----------

input_frame = tk.Frame(
    home_frame,
    bg="white",
    padx=40,
    pady=25
)

input_frame.pack()


# Upload Button

upload_button = tk.Button(
    input_frame,
    text="Upload CSV File",
    command=upload_csv,
    bg="#3B7C96",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=7
)

upload_button.pack(pady=5)


# Status Label

status_label = tk.Label(
    input_frame,
    text="No file selected",
    font=("Arial", 10, "italic"),
    fg="gray",
    bg="white"
)

status_label.pack(pady=8)



# Comment Label

comment_label = tk.Label(
    input_frame,
    text="Enter Comment:",
    bg="white",
    font=("Arial", 10, "bold")
)

comment_label.pack(pady=(15, 5))


# Comment Box

comment_box = tk.Text(
    input_frame,
    height=5,
    width=55
)

comment_box.pack()


# Add Comment Button

add_comment_button = tk.Button(
    input_frame,
    text="Add Comment",
    command=add_comment,
    fg="#3B7C96",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5
)

add_comment_button.pack(pady=12)


# Analyze Button

analyze_button = tk.Button(
    home_frame,
    text="ANALYZE",
    command=show_results,
    bg="#3B7C96",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=25,
    pady=8
)

analyze_button.pack(pady=25)


# ==================================================
#                    RESULT PAGE
# ==================================================

result_frame = tk.Frame(
    root,
    bg="#EFF7FF"
)


# Result Title

result_title = tk.Label(
    result_frame,
    text="SENTIMENT ANALYSIS RESULTS",
    font=("Book Antiqua", 24, "bold"),
    bg="#EFF7FF",
    fg="#558CBD"
)

result_title.pack(pady=(50, 10))


result_subtitle = tk.Label(
    result_frame,
    text="Overall Sentiment Analysis",
    font=("Book Antiqua", 14, "italic"),
    bg="#EFF7FF",
    fg="#558CBD"
)

result_subtitle.pack(pady=10)


# Result Cards Frame

cards_frame = tk.Frame(
    result_frame,
    bg="#EFF7FF"
)

cards_frame.pack(pady=40)


# Positive Card

positive_card = tk.Label(
    cards_frame,
    text="POSITIVE\n\n--",
    font=("Arial", 14, "bold"),
    bg="white",
    width=15,
    height=5
)

positive_card.pack(side="left", padx=15)


# Negative Card

negative_card = tk.Label(
    cards_frame,
    text="NEGATIVE\n\n--",
    font=("Arial", 14, "bold"),
    bg="white",
    width=15,
    height=5
)

negative_card.pack(side="left", padx=15)


# Neutral Card

neutral_card = tk.Label(
    cards_frame,
    text="NEUTRAL\n\n--",
    font=("Arial", 14, "bold"),
    bg="white",
    width=15,
    height=5
)

neutral_card.pack(side="left", padx=15)


# Buttons Frame

result_button_frame = tk.Frame(
    result_frame,
    bg="#EFF7FF"
)

result_button_frame.pack(pady=30)


# View Graph Button

view_graph_button = tk.Button(
    result_button_frame,
    text="View Graph",
    command=show_graph,
    fg="#3B7C96",
    font=("Book Antiqua", 10, "italic"),
    padx=15,
    pady=7
)

view_graph_button.pack(side="left", padx=10)


# Back Button

back_home_button = tk.Button(
    result_button_frame,
    text="← Back",
    command=back_to_home,
    fg="#3B7C96",
    font=("Book Antiqua", 10, "italic"),
    padx=15,
    pady=7
)

back_home_button.pack(side="left", padx=10)


# ==================================================
#                    GRAPH PAGE
# ==================================================

graph_frame = tk.Frame(
    root,
    bg="white"
)


# Graph Title

graph_title = tk.Label(
    graph_frame,
    text="SENTIMENT ANALYSIS DASHBOARD",
    font=("Arial", 22, "bold"),
    bg="white",
    fg="#558CBD"
)

graph_title.pack(pady=40)


# Temporary message

graph_message = tk.Label(
    graph_frame,
    text="Graphs will be displayed here",
    font=("Arial", 16),
    bg="white"
)

graph_message.pack(pady=50)


# Back to Results Button

back_result_button = tk.Button(
    graph_frame,
    text="← Back to Results",
    command=back_to_results,
    fg="#3B7C96",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=7
)

back_result_button.pack(pady=20)


# ================= START APPLICATION =================

root.mainloop()
