# Social Media Sentiment Analysis: Technical Backlog & Pending Roadmap

> **Document Type:** Project Development Roadmap & Technical Backlog  
> **Target Release:** v1.1.0 & v2.0.0  
> **Status:** Open / Active Development  
> **Last Updated:** July 29, 2026  

---

## 1. Technical Task Backlog & Feature Matrix

| Priority | Feature / Task Area | Target Package / Files | Technical Scope & Description | Estimated Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **High** | **Data & Report Export** | [src/ui/ui_manager.py](file:///c:/Users/risha/Desktop/SF%20Project/social-media-analytics/src/ui/ui_manager.py)<br>[src/utils/helpers.py](file:///c:/Users/risha/Desktop/SF%20Project/social-media-analytics/src/utils/helpers.py) | Add one-click export buttons to save analyzed dataset predictions and summary statistics to Excel (`.xlsx`) and CSV format. | Low (1–2 hrs) |
| **High** | **Instant Single-Comment Predictor Card** | [src/ui/ui_manager.py](file:///c:/Users/risha/Desktop/SF%20Project/social-media-analytics/src/ui/ui_manager.py)<br>[src/core/predict.py](file:///c:/Users/risha/Desktop/SF%20Project/social-media-analytics/src/core/predict.py) | Integrate a real-time single comment text box on the home screen for instant sentiment prediction without requiring file uploads. | Low (1–2 hrs) |
| **Medium** | **Multi-Model Benchmarking Suite** | `src/core/benchmark.py` | Develop automated evaluation script comparing Logistic Regression performance against Random Forest, Naive Bayes, and SVM classifiers. | Medium (2–3 hrs) |
| **Medium** | **Standalone `.exe` Distribution Build** | `build_exe.py` | Configure PyInstaller packaging script to bundle Python runtime, Tkinter GUI, and trained model binaries into a standalone Windows executable. | Medium (2–3 hrs) |
| **Low** | **Multi-Language Text Support** | [src/core/preprocess.py](file:///c:/Users/risha/Desktop/SF%20Project/social-media-analytics/src/core/preprocess.py) | Extend text normalization and vectorization pipeline to support multi-lingual social media text (e.g., Hindi, Spanish). | High (4+ hrs) |

---

## 2. Detailed Feature Specifications

### 2.1 One-Click Data & Report Export (v1.1.0)
- **Objective:** Allow users to export predicted sentiment results (`Original Comment`, `Cleaned Comment`, `Sentiment`) and aggregated statistics to Excel (`.xlsx`) or PDF format.
- **Implementation Strategy:**
  - Add `openpyxl` / `pandas` export helper in [src/utils/helpers.py](file:///c:/Users/risha/Desktop/SF%20Project/social-media-analytics/src/utils/helpers.py).
  - Add "Export to Excel" button in `SentimentApp.render_dashboard()` in [src/ui/ui_manager.py](file:///c:/Users/risha/Desktop/SF%20Project/social-media-analytics/src/ui/ui_manager.py).

### 2.2 Instant Single-Comment Predictor Card (v1.1.0)
- **Objective:** Provide instant sentiment classification for single text inputs without requiring a full CSV file upload.
- **Implementation Strategy:**
  - Connect text box input in `_init_home_view()` directly to `predict_single_comment(text)`.
  - Display predicted sentiment pill (Positive / Negative / Neutral) with confidence score.

### 2.3 Standalone Executable Packaging (`.exe`) (v1.2.0)
- **Objective:** Package the entire Tkinter GUI, Python environment, and pre-trained machine learning model into a portable `.exe` binary for non-technical users.
- **Implementation Strategy:**
  - Create `build.py` using `pyinstaller --noconsole --onefile app.py`.
  - Ensure static asset paths and `.pkl` model files resolve correctly using relative bundle paths.

---

*End of Technical Backlog.*
