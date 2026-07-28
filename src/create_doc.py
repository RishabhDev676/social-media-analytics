from docx import Document
from docx.shared import Pt, RGBColor
import os

def add_heading(doc, text, level=1):
    heading = doc.add_heading(text, level=level)
    for run in heading.runs:
        run.font.color.rgb = RGBColor(0, 51, 102)

def add_paragraph(doc, text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    if bold:
        run.bold = True
    return p

def add_code(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(10)
    p.style = 'Intense Quote'

def main():
    doc = Document()
    
    # Title
    add_heading(doc, 'Social Media Sentiment Analysis: Full Project Guide', level=0)
    add_paragraph(doc, 'This document explains every file in our project in simple, easy-to-understand terms. This will help you understand how the code works from start to finish.', bold=True)
    
    # Overview
    add_heading(doc, '1. Project Overview', level=1)
    doc.add_paragraph("Our project takes social media comments and predicts whether they are Positive, Negative, or Neutral. We do this in several steps, separated into different Python files:")
    doc.add_paragraph("• preprocessing.py: Cleans up messy text.")
    doc.add_paragraph("• train_model.py: Teaches the AI using our 11,000 comment dataset.")
    doc.add_paragraph("• predict.py: Uses the trained AI to analyze new comments.")
    doc.add_paragraph("• statistics.py: Crunches the numbers to show overall sentiment.")
    doc.add_paragraph("• gui.py: Provides a visual app for the user to upload files.")

    # Preprocessing
    add_heading(doc, '2. preprocessing.py (Cleaning the Data)', level=1)
    add_paragraph(doc, "People type messily on social media. Before the AI can read it, we have to clean the text.")
    add_code(doc, "text = re.sub(r\"http\S+|www\S+|https\S+\", \"\", text)\ntext = re.sub(r\"[^a-zA-Z\s]\", \"\", text)\nwords = [word for word in words if word not in stop_words]")
    doc.add_paragraph("• We use 're' (Regular Expressions) to search and destroy web links (URLs).")
    doc.add_paragraph("• We delete all punctuation, numbers, and emojis so only English letters remain.")
    doc.add_paragraph("• We use the 'NLTK' library to remove \"stop words.\" Stop words are common words like \"the\", \"and\", or \"is\" that don't tell us anything about sentiment.")

    # Training
    add_heading(doc, '3. train_model.py (Teaching the AI)', level=1)
    add_paragraph(doc, "This script loads our huge 11,000-comment dataset and trains a Machine Learning model.")
    add_code(doc, "vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')\nX = vectorizer.fit_transform(df[\"cleaned_comment\"])\n\nmodel = LogisticRegression(max_iter=1000)\nmodel.fit(X_train, y_train)")
    doc.add_paragraph("• TfidfVectorizer: The AI doesn't understand words, only math. This tool converts our sentences into numerical scores. 'ngram_range=(1, 2)' means it looks at single words AND pairs of words (like \"not good\").")
    doc.add_paragraph("• Logistic Regression: This is our AI brain. We show it 80% of our data (the training set) and say, \"Find the mathematical pattern that makes a comment Positive or Negative.\"")
    doc.add_paragraph("• Once trained, our model achieved a ~94.8% accuracy on the test exam! We then use 'joblib.dump' to save this trained brain into '.pkl' files so we don't have to retrain it every time.")

    # Prediction
    add_heading(doc, '4. predict.py (Making New Guesses)', level=1)
    add_paragraph(doc, "Now that the AI is smart and saved to a file, this script loads it up to analyze brand-new comments.")
    add_code(doc, "model = joblib.load(model_path)\nvectorizer = joblib.load(vectorizer_path)\n\ntext_features = vectorizer.transform([cleaned_text])\nprediction = model.predict(text_features)")
    doc.add_paragraph("• joblib.load: Wakes up our saved model from the hard drive.")
    doc.add_paragraph("• vectorizer.transform: Turns the new user comment into math numbers exactly the same way we did during training.")
    doc.add_paragraph("• model.predict: The AI looks at the numbers and spits out a final guess: Positive, Negative, or Neutral.")

    # Statistics
    add_heading(doc, '5. statistics.py (Crunching the Numbers)', level=1)
    add_paragraph(doc, "Once we have predictions for hundreds of comments, we want to see the big picture.")
    add_code(doc, "counts = df[\"sentiment\"].value_counts()\npositive_pct = (positive_count / total) * 100")
    doc.add_paragraph("• We use the 'Pandas' library to count how many comments fell into each bucket.")
    doc.add_paragraph("• We calculate percentages to show the user exactly what portion of their audience is happy versus unhappy.")

    # GUI
    add_heading(doc, '6. gui.py (The Visual App)', level=1)
    add_paragraph(doc, "Users don't want to type code; they want buttons to click. We built a desktop app using 'Tkinter'.")
    add_code(doc, "import tkinter as tk\nfrom tkinter import filedialog\n\nfile_path = filedialog.askopenfilename()")
    doc.add_paragraph("• Tkinter (tk): This is Python's built-in tool for drawing windows, buttons, and text boxes.")
    doc.add_paragraph("• filedialog: This opens up your computer's standard file browser so the user can visually select their CSV file to upload.")
    doc.add_paragraph("• When the user clicks 'Upload', our app grabs the file, runs it through predict.py, and displays the results!")

    # Save Document
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(base_dir, "..", "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    output_path = os.path.join(docs_dir, "Model_Explanation.docx")
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    main()
