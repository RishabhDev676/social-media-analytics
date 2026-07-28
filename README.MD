# 📊 Social Media Sentiment Analysis

A Python-based desktop application that analyzes social media data using Machine Learning and Statistical Analysis. The application processes social media posts, predicts sentiment, generates statistical insights, and presents the results through an interactive graphical dashboard.

---

## 🚀 Features

- **One-Click Launch:** Simply run `python app.py` to start the entire dashboard.
- **Smart Model Manager:** Automatically detects missing models, trains them in the background, and caches them for fast predictions.
- **Asynchronous Execution:** Heavy machine learning computations run in background threads with a responsive Loading Screen.
- **Text Preprocessing:** Automatically cleans data (lowercase, removes URLs, punctuation, stopwords).
- **Sentiment Analysis:** Powered by Logistic Regression and TF-IDF feature extraction.
- **Statistical Analysis:** Calculates sentiment distribution, total counts, and dominant sentiment.
- **Interactive Dashboard:** View processed comments, clean text, and sentiment scores in a scrollable data table alongside summary stat cards.

---

## 🛠️ Technologies Used

- **Python** 
- **Tkinter (ttk)** (Modern GUI)
- **Pandas** (Data handling)
- **Scikit-learn** (TF-IDF, Logistic Regression)
- **Joblib** (Model saving/loading)
- **Threading** (Asynchronous operations)

---

## 📂 Clean Architecture Structure

```
social-media-analytics/
│
├── app.py                     ← Application entry point (One-command launch)
├── data/                      
│   ├── raw/                   ← Raw training data
│   └── uploaded/              ← CSV files for testing
│
├── models/                    
│   ├── sentiment_model.pkl    ← Auto-managed Logistic Regression model
│   └── vectorizer.pkl         ← Auto-managed TF-IDF vectorizer
│
├── src/
│   ├── analytics/             
│   │   └── statistics.py      ← Statistical data calculation
│   ├── core/                  
│   │   ├── pipeline.py        ← Glues prediction and statistics together
│   │   ├── predict.py         ← Prediction functions
│   │   ├── preprocess.py      ← Text cleaning functions
│   │   ├── train.py           ← Model training logic
│   │   └── model_manager.py   ← Model lifecycle auto-manager
│   ├── ui/                    
│   │   └── ui_manager.py      ← Object-Oriented Tkinter Dashboard
│   └── utils/
│       └── helpers.py         ← Utility scripts
│
├── docs/                      ← Project documentation
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/RishabhDev676/social-media-analytics.git
cd social-media-analytics
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

Thanks to the new architecture, you no longer have to manually set the `PYTHONPATH` or manually train the models. The application handles everything automatically!

Launch the application with a single command from the root directory:

```bash
python app.py
```

### What happens when you run it?
1. The app automatically configures its environment.
2. The Tkinter Dashboard opens.
3. You can browse and select a CSV file.
4. When you click **Analyze**, the `ModelManager` checks if the `.pkl` models exist. If they don't, it trains them invisibly in the background.
5. The pipeline processes the CSV, predicts sentiments, and calculates stats.
6. The Dashboard renders the clean statistics and data table!

---

## 📈 Pipeline Workflow

```
app.py (Entry Point)
      ↓
User Uploads CSV via UI
      ↓
src.core.pipeline.py 
      ↓
src.core.predict.py (Fetches models via ModelManager)
      ↓
src.analytics.statistics.py (Calculates summary stats)
      ↓
Clean Data & Stats Dictionary Returned
      ↓
Rendered by src.ui.ui_manager.py (Dashboard)
```

---

## 👥 Team Members & Contributions

| Member | Role |
|--------|------|
| **Rishabh** | TF-IDF, Logistic Regression training, core architecture |
| **Swarni** | Dataset collection and preprocessing |
| **Daksha** | GUI design, layout, and UX threading |
| **Prathamesh** | Prediction integration and Model Manager |
| **Manvi** | Statistical analysis pipeline |

*(Note: Data Visualization was deprecated as part of the phase 7 redesign to prioritize clean statistical cards).*

---

## 📄 License

This project is developed for academic purposes as part of the Statistical Fundamentals course.