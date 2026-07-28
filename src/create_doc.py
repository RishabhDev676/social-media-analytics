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
    add_heading(doc, 'Sentiment Analysis Model: Code Explanation', level=0)
    add_paragraph(doc, 'This document provides a simple and detailed explanation of our sentiment analysis model, focusing on the steps immediately following data preprocessing.', bold=True)
    
    # Section 1: The Imports
    add_heading(doc, '1. The Imports (The Tools We Use)', level=1)
    add_paragraph(doc, "Before we do anything, we need to import the right tools into Python. Think of imports like pulling out different tools from a toolbox.")
    
    add_code(doc, "import joblib\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import accuracy_score, classification_report")
    
    doc.add_paragraph("• joblib: A tool used to save (or \"dump\") our trained model so we can use it later without retraining it from scratch.")
    doc.add_paragraph("• sklearn (Scikit-Learn): This is the main machine learning library in Python. We import several specific tools from it:")
    doc.add_paragraph("  - TfidfVectorizer: This translates our text comments into numbers so the math model can understand them.")
    doc.add_paragraph("  - train_test_split: This cuts our dataset into two pieces: one for learning (training) and one for a final exam (testing).")
    doc.add_paragraph("  - LogisticRegression: The actual brain/algorithm that will learn how to guess the sentiment.")
    doc.add_paragraph("  - accuracy_score & classification_report: Tools to check the model's \"report card\" and see how well it performed.")

    # Section 2: Feature Extraction (TF-IDF)
    add_heading(doc, '2. Feature Extraction (Turning Text into Numbers)', level=1)
    add_paragraph(doc, "Machine learning models cannot read English words like \"good\" or \"terrible.\" They only understand numbers. Feature extraction translates the text into a numerical format.")
    
    add_code(doc, "vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english', max_features=5000)\nX = vectorizer.fit_transform(df[\"cleaned_comment\"])\ny = df[\"sentiment\"]")
    
    doc.add_paragraph("• TfidfVectorizer: We use a technique called TF-IDF (Term Frequency-Inverse Document Frequency). It looks at how often a word appears in a comment but scales it down if the word is too common across all comments (like \"the\", \"is\").")
    doc.add_paragraph("• stop_words='english': Automatically ignores common English words (like \"and\", \"the\") that don't help determine sentiment.")
    doc.add_paragraph("• ngram_range=(1,2): Instead of just looking at single words (like \"not\" and \"good\"), it also looks at pairs of words together (like \"not good\"). This captures a lot more context!")
    doc.add_paragraph("• X: This is our new matrix of numbers (features) representing all the comments.")
    doc.add_paragraph("• y: This is the actual answer key (the sentiments: Positive, Negative, Neutral).")

    # Section 3: Train-Test Split
    add_heading(doc, '3. Train-Test Split (Preparing for the Exam)', level=1)
    add_paragraph(doc, "If we let the model learn on all our data, we wouldn't have any unseen data left to test it on. It would be like giving a student the exam questions to study with!")
    
    add_code(doc, "X_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42\n)")
    
    doc.add_paragraph("• We use train_test_split to chop our data into two groups.")
    doc.add_paragraph("• test_size=0.2: This means 80% of our 11,000 comments (8,800) will be used to train the model, and 20% (2,200) will be hidden away as the final test.")
    doc.add_paragraph("• random_state=42: This just ensures the data is shuffled exactly the same way every time we run the code.")

    # Section 4: Training the Model
    add_heading(doc, '4. Training the Model (Logistic Regression)', level=1)
    add_paragraph(doc, "Now we actually build and train the AI.")
    
    add_code(doc, "model = LogisticRegression(max_iter=1000)\nmodel.fit(X_train, y_train)")
    
    doc.add_paragraph("• Logistic Regression: Despite the word 'regression', this is an algorithm used for classification. It tries to draw statistical lines between what makes a comment Positive, Negative, or Neutral based on the numerical TF-IDF scores.")
    doc.add_paragraph("• model.fit(X_train, y_train): This is where the actual learning happens. We feed the model the training data (X_train) and the correct answers (y_train). The model adjusts its internal math to get the answers right as often as possible.")

    # Section 5: Model Evaluation
    add_heading(doc, '5. Evaluating the Model (The Final Exam)', level=1)
    add_paragraph(doc, "Once the model has learned, we need to test it on the 20% of data it has never seen before.")
    
    add_code(doc, "y_pred = model.predict(X_test)\naccuracy = accuracy_score(y_test, y_pred)\nprint(classification_report(y_test, y_pred))")
    
    doc.add_paragraph("• model.predict(X_test): We give the model the unseen test comments and ask it to predict the sentiments.")
    doc.add_paragraph("• accuracy_score: We compare the model's guesses (y_pred) to the actual real answers (y_test). Our model gets an accuracy of about 94.8%!")
    doc.add_paragraph("• classification_report: This prints out a detailed breakdown showing how well the model performed on each specific category (Positive vs. Negative vs. Neutral).")

    # Section 6: Saving the Model
    add_heading(doc, '6. Saving the Model for the Future', level=1)
    add_paragraph(doc, "Finally, we don't want to retrain the model every single time we want to predict a new tweet or comment.")
    
    add_code(doc, "joblib.dump(model, model_path)\njoblib.dump(vectorizer, vectorizer_path)")
    
    doc.add_paragraph("• joblib.dump: This compresses and saves both our trained Logistic Regression model and our TF-IDF Vectorizer into physical files (.pkl files).")
    doc.add_paragraph("• When we want to use the app in the future, we just load these files, and the model instantly remembers everything it learned.")

    # Save Document
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(base_dir, "..", "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    output_path = os.path.join(docs_dir, "Model_Explanation.docx")
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    main()
