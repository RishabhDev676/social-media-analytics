# 📊 Social Media Sentiment Analysis

A Python-based desktop application that analyzes social media data using Machine Learning, Statistical Analysis, and Data Visualization. The application processes social media posts, predicts sentiment, generates statistical insights, and presents the results through an interactive graphical interface.

---

## 🚀 Features

- Upload CSV datasets
- Text preprocessing (lowercase, remove URLs, punctuation, stopwords)
- Sentiment Analysis using Logistic Regression (ML)
- TF-IDF Feature Extraction
- Statistical Analysis (counts, percentages)
- Interactive Charts & Graphs (Pie, Bar, Histogram)
- User-friendly GUI using Tkinter

---

## 🛠️ Technologies Used

- Python
- Tkinter (GUI)
- Pandas (Data handling)
- NumPy (Numerical operations)
- Scikit-learn (TF-IDF, Logistic Regression, train-test split)
- Matplotlib (Charts)
- NLTK (Stopwords removal)
- Joblib (Model saving/loading)

---

## 📂 Project Structure

```
social-media-analytics/
│
├── data/
│   ├── comments.csv              ← Training dataset (60 labeled comments)
│   ├── test_100_comments.csv     ← Test dataset (105 unlabeled comments)
│   └── predicted_sentiments.csv  ← Output dataset with actual sentiments for stats/charts
│
├── models/
│   ├── model.pkl                 ← Trained Logistic Regression model
│   └── vectorizer.pkl            ← Fitted TF-IDF vectorizer
│
├── src/
│   ├── preprocessing.py          ← Text cleaning functions
│   ├── train_model.py            ← TF-IDF + Logistic Regression training pipeline
│   ├── predict.py                ← Load model and predict sentiments
│   ├── statistics.py             ← Statistical analysis (pending)
│   ├── visualization.py          ← Charts and graphs (pending)
│   ├── gui.py                    ← Tkinter GUI
│   └── create_doc.py             ← Script to generate documentation
│
├── docs/
│   ├── Change_Report.docx        ← Report of all changes made
│   ├── Model_Explanation.docx    ← Explains how code and ML models work
│   └── Pending_Work_Team_Guide.docx ← Guide for remaining work
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/RishabhDev676/social-media-analytics.git
```

Move into the project folder

```bash
cd social-media-analytics
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

**Step 1:** Train the model (run once)

```bash
cd src
python train_model.py
```

This creates `models/model.pkl` and `models/vectorizer.pkl`.

**Step 2:** Test predictions

```bash
python predict.py
```

**Step 3:** Launch the GUI

```bash
python gui.py
```

---

## 📈 Workflow

```
CSV File (data/comments.csv)
      ↓
Pandas DataFrame
      ↓
Text Preprocessing (preprocessing.py)
      ↓
Cleaned Comments
      ↓
TF-IDF Vectorization (train_model.py)
      ↓
Numerical Feature Matrix
      ↓
Train/Test Split (80/20)
      ↓
Logistic Regression Training
      ↓
Saved model.pkl + vectorizer.pkl
      ↓
User Input / CSV → predict.py → Sentiment Result
      ↓
Saved predicted_sentiments.csv
      ↓
Statistical Analysis (statistics.py)
      ↓
Charts & Visualization (visualization.py)
      ↓
Results Displayed in GUI (gui.py)
```

---

## 🤖 Machine Learning

The project uses **Logistic Regression** to classify social media posts into:

- **Positive**
- **Negative**
- **Neutral**

Feature extraction is done using **TF-IDF (Term Frequency - Inverse Document Frequency)**.

---

## 📊 Statistical Analysis

The application calculates:

- Total comments
- Positive / Negative / Neutral count
- Positive / Negative / Neutral percentage

---

## 📉 Visualizations

- Pie Chart (sentiment distribution)
- Bar Chart (sentiment counts)
- Histogram (comment length distribution)

---

## ✅ Module Status

| Module | Owner | Status |
|--------|-------|--------|
| `data/comments.csv` | Swarni | ✅ Done |
| `preprocessing.py` | Swarni | ✅ Done |
| `train_model.py` | Rishabh | ✅ Done |
| `predict.py` | Prathamesh | ✅ Done |
| `gui.py` (basic) | Daksha | ✅ Done |
| `statistics.py` | Manvi | ⏳ Pending |
| `visualization.py` | Sai | ⏳ Pending |
| `gui.py` (full integration) | Daksha + Prathamesh | ⏳ Pending |

---

## 🚀 Getting Started for Team Members

### Step 1: Clone the repo (first time only)

```bash
git clone https://github.com/RishabhDev676/social-media-analytics.git
cd social-media-analytics
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Train the model to generate model files

```bash
cd src
python train_model.py
```

You should see all 7 steps run and `model.pkl` + `vectorizer.pkl` created in the `models/` folder.

### Step 4: Verify everything works

```bash
python predict.py
```

You should see:
```
Comment: I really enjoyed the movie, it was fantastic!
Predicted Sentiment: Positive

Comment: Terrible experience, worst product ever
Predicted Sentiment: Negative
```

### Step 5: Work on your assigned module

Now start coding your file. See the sections below for your specific instructions.

---

## 👩‍💻 Manvi — statistics.py

**What to do:** Create a function `compute_statistics(df)` that takes a DataFrame with a `sentiment` column and returns a dictionary with counts and percentages.

**How to test:**
```bash
cd src
python statistics.py
```

**Detailed guide:** Read `docs/Pending_Work_Team_Guide.docx` — Section 2

---

## 👨‍💻 Sai — visualization.py

**What to do:** Create 3 functions using Matplotlib:
- `create_pie_chart(stats)` — Pie chart of sentiment percentages
- `create_bar_chart(stats)` — Bar chart of sentiment counts
- `create_histogram(df)` — Histogram of comment lengths

**How to test:**
```bash
cd src
python visualization.py
```

**Detailed guide:** Read `docs/Pending_Work_Team_Guide.docx` — Section 3

---

## 👩‍💻 Daksha + Prathamesh — gui.py (Full Integration)

**What to do:**
- **Daksha:** Build the GUI layout — add text entry box, results table, stats panel, chart buttons
- **Prathamesh:** Wire up the buttons — connect predict.py, statistics.py, and visualization.py to the GUI

**How to test:**
```bash
cd src
python gui.py
```

**Detailed guide:** Read `docs/Pending_Work_Team_Guide.docx` — Section 4

---

## 📝 Git Commands for Team

**Before starting work (always pull latest code first):**
```bash
git pull origin main
```

**After finishing your file:**
```bash
git add src/your_file.py
git commit -m "feat: implement your_module_name"
git push origin main
```

**If you get a merge conflict:**
```bash
git pull origin main
# Fix the conflict in the file manually
git add .
git commit -m "fix: resolve merge conflict"
git push origin main
```

---

## 👥 Team Members

| Member | Role |
|--------|------|
| Rishabh | TF-IDF, Logistic Regression training, model saving |
| Swarni | Dataset collection and preprocessing |
| Daksha | GUI design and layout |
| Prathamesh | Prediction and GUI integration |
| Manvi | Statistical analysis |
| Sai | Charts and dashboard |

---

## 📌 Future Scope

- Real-time Twitter/X sentiment analysis
- Dashboard
- Deep Learning models
- Word Cloud generation
- Multiple language support
- Export reports as PDF

---

## 📄 License

This project is developed for academic purposes as part of the Statistical Fundamentals course.