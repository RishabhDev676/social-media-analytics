import os
import sys
from unittest.mock import patch

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ui.ui_manager import SentimentApp


class DummyLabel:
    def __init__(self):
        self.text = ""
        self.text_color = None

    def configure(self, **kwargs):
        if "text" in kwargs:
            self.text = kwargs["text"]
        if "text_color" in kwargs:
            self.text_color = kwargs["text_color"]


class DummyTextbox:
    def __init__(self, value=""):
        self.value = value

    def get(self, start, end):
        return self.value

    def delete(self, start, end):
        self.value = ""


class DummyMessageBox:
    def showerror(self, *args, **kwargs):
        return None

    def showwarning(self, *args, **kwargs):
        return None

    def showinfo(self, *args, **kwargs):
        return None


def test_show_frame_switches_between_frames():
    app = SentimentApp.__new__(SentimentApp)

    class DummyFrame:
        def __init__(self):
            self.pack_called = False

        def pack(self, *args, **kwargs):
            self.pack_called = True

        def pack_forget(self):
            self.pack_called = False

    app.frames = {"Home": DummyFrame(), "Upload": DummyFrame()}
    app.current_frame_name = None

    app.show_frame("Home")
    assert app.current_frame_name == "Home"

    app.show_frame("Home")
    assert app.current_frame_name == "Home"


def test_upload_csv_updates_status_label(tmp_path):
    app = SentimentApp.__new__(SentimentApp)
    app.selected_file = None
    app.status_label = DummyLabel()

    csv_path = tmp_path / "comments.csv"
    csv_path.write_text("comment\nhello\n", encoding="utf-8")

    with patch("src.ui.ui_manager.filedialog.askopenfilename", return_value=str(csv_path)):
        app.upload_csv()

    assert app.status_label.text == f"Selected: {csv_path.name}"


def test_add_comment_appends_to_selected_csv(tmp_path):
    app = SentimentApp.__new__(SentimentApp)
    csv_path = tmp_path / "comments.csv"
    csv_path.write_text("ID,comment,sentiment\n1,hello,\n", encoding="utf-8")

    app.selected_file = str(csv_path)
    app.comment_box = DummyTextbox("New manual comment")

    with patch("src.ui.ui_manager.messagebox", DummyMessageBox()):
        app.add_comment()

    updated_df = pd.read_csv(csv_path)
    assert updated_df.iloc[-1]["comment"] == "New manual comment"
    assert str(updated_df.iloc[-1]["sentiment"]).strip() in {"", "nan"}
