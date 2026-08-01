# 📊 Social Media Sentiment Analysis

A Python-based desktop application that analyzes social media data using Machine Learning and Statistical Analysis. The application processes social media posts, predicts sentiment, generates statistical insights, and presents the results through an interactive graphical dashboard.

---

## 🚀 Features

- **One-Click Launch:** Run `python app.py` to start the desktop app.
- **Modern Multi-Page GUI:** The application now opens with a homepage, then moves to an upload page, then a results page.
- **CustomTkinter UI:** The screen layout uses CustomTkinter for a cleaner and more modern interface.
- **Smart Model Manager:** Automatically detects missing models, trains them in the background, and caches them for fast predictions.
- **Asynchronous Execution:** Heavy machine learning work runs in background threads while a loading screen is shown.
- **Text Preprocessing:** Removes URLs, punctuation, and stopwords before prediction.
- **Sentiment Analysis:** Uses TF-IDF + Logistic Regression for classification.
- **Statistical Analysis:** Shows sentiment counts, percentages, dominant sentiment, and text-length stats.
- **Result Actions:** From the results page you can open plots, report details, and the processed data table.

---

## 🛠️ Technologies Used

- **Python**
- **CustomTkinter** (modern GUI widgets)
- **Tkinter/ttk** (progress bars, treeviews, dialogs)
- **Pandas** (data handling)
- **Scikit-learn** (TF-IDF, Logistic Regression)
- **Joblib** (model saving/loading)
- **Matplotlib** (plots)
- **Threading** (background processing)

---

## 📂 Project Architecture

```
social-media-analytics/
│
├── app.py                     ← Entry point for the desktop app
├── data/
│   ├── raw/                   ← Raw training data
│   ├── processed/             ← Saved prediction output
│   └── uploaded/              ← CSV files chosen by the user
├── models/                    ← Trained ML model files
├── src/
│   ├── gui.py                 ← Modern CustomTkinter GUI wrapper
│   ├── launcher.py            ← Application launcher logic
│   ├── statistics_module.py   ← Core statistics computations
│   ├── analytics/
│   │   └── statistics.py      ← Extended analytics calculations
│   ├── core/
│   │   ├── pipeline.py        ← Main analysis pipeline
│   │   ├── predict.py         ← Prediction logic
│   │   ├── preprocess.py      ← Text cleaning logic
│   │   ├── train.py           ← Model training logic
│   │   └── model_manager.py   ← Model loading/training manager
│   ├── ui/
│   │   └── ui_manager.py      ← All GUI pages: Home, Upload, Loading, Results
│   └── utils/
│       ├── helpers.py
│       ├── create_doc.py
│       ├── create_change_report.py
│       └── create_pending_work_doc.py
├── tests/                     ← Automated testing suite
│   └── test_ui_flow.py        ← UI navigation flow tests
├── docs/                      ← Project documentation
├── requirements.txt
└── README.md
```

---

## 🧭 Where to Edit Different Parts

### 1. Homepage UI
Edit [src/ui/ui_manager.py](src/ui/ui_manager.py) and change the `_init_home_view()` method.

### 2. Upload Page UI
Edit [src/ui/ui_manager.py](src/ui/ui_manager.py) and change the `_init_upload_view()` method.

### 3. Results Page UI
Edit [src/ui/ui_manager.py](src/ui/ui_manager.py) and change the `_init_results_view()` method plus `render_results()`.

### 4. Buttons on the Results Page
Edit [src/ui/ui_manager.py](src/ui/ui_manager.py) for:
- `show_plots()`
- `show_report()`
- `show_data_table()`
- `_build_report_text()`

### 5. Analysis Logic
Edit the ML/backend flow in:
- [src/core/pipeline.py](src/core/pipeline.py)
- [src/core/predict.py](src/core/predict.py)
- [src/core/preprocess.py](src/core/preprocess.py)
- [src/analytics/statistics.py](src/analytics/statistics.py)

### 6. Data Files
Use the CSV files in [data/raw](data/raw), [data/uploaded](data/uploaded), and [data/processed](data/processed) for testing and sample input.

---

## 🔄 Current UI Flow

1. The app opens on the Home page.
2. Click the upload button to choose a CSV file.
3. Click Analyze Sentiments.
4. The app shows a loading screen.
5. After analysis finishes, the Results page opens.
6. From the Results page, you can view plots, the report, or the processed data.

This is implemented in [src/ui/ui_manager.py](src/ui/ui_manager.py).

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
| **Sai** | Data analytics and visualization components |

---

## 📄 License

This project is developed for academic purposes as part of the Statistical Fundamentals course.