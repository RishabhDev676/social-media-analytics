import pandas as pd
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from preprocessing import preprocess_dataframe


# -----------------------------------------------
# STEP 1: LOAD THE DATASET
# -----------------------------------------------
print("=" * 50)
print("STEP 1: Loading Dataset")
print("=" * 50)

# Build the path to the data file
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "..", "data", "comments.csv")

# Read the CSV file into a DataFrame
df = pd.read_csv(data_path)

print(f"Dataset loaded successfully!")
print(f"Total comments: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"\nFirst 5 rows:")
print(df.head())


# -----------------------------------------------
# STEP 2: PREPROCESS THE TEXT
# -----------------------------------------------
print("\n" + "=" * 50)
print("STEP 2: Preprocessing Text")
print("=" * 50)

# Apply preprocessing to all comments
# This adds a 'cleaned_comment' column to the DataFrame
df = preprocess_dataframe(df, column="comment")

print("Preprocessing complete!")
print(f"\nSample - Original vs Cleaned:")
for i in range(3):
    print(f"  Original: {df['comment'].iloc[i]}")
    print(f"  Cleaned:  {df['cleaned_comment'].iloc[i]}")
    print()


# -----------------------------------------------
# STEP 3: FEATURE EXTRACTION (TF-IDF)
# -----------------------------------------------
print("=" * 50)
print("STEP 3: Feature Extraction (TF-IDF)")
print("=" * 50)

# Create the TF-IDF Vectorizer
# This converts text into numerical features
vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english', max_features=5000)

# X = the numerical feature matrix (input for the model)
# We use the cleaned comments, not the raw ones
X = vectorizer.fit_transform(df["cleaned_comment"])

# y = the sentiment labels (what we want to predict)
y = df["sentiment"]

print(f"Feature matrix shape: {X.shape}")
print(f"  - {X.shape[0]} comments")
print(f"  - {X.shape[1]} unique words (features)")
print(f"Labels: {list(y.unique())}")


# -----------------------------------------------
# STEP 4: TRAIN-TEST SPLIT
# -----------------------------------------------
print("\n" + "=" * 50)
print("STEP 4: Train-Test Split (80/20)")
print("=" * 50)

# Split data into training (80%) and testing (20%)
# random_state=42 ensures we get the same split every time
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training data: {X_train.shape[0]} comments")
print(f"Testing data:  {X_test.shape[0]} comments")


# -----------------------------------------------
# STEP 5: TRAIN THE MODEL (Logistic Regression)
# -----------------------------------------------
print("\n" + "=" * 50)
print("STEP 5: Training Logistic Regression Model")
print("=" * 50)

# Create the Logistic Regression model
model = LogisticRegression(max_iter=1000)

# Train (fit) the model using training data
model.fit(X_train, y_train)

print("Model training complete!")


# -----------------------------------------------
# STEP 6: EVALUATE THE MODEL
# -----------------------------------------------
print("\n" + "=" * 50)
print("STEP 6: Model Evaluation")
print("=" * 50)

# Predict sentiments on the test data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Detailed classification report
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred))


# -----------------------------------------------
# STEP 7: SAVE THE MODEL AND VECTORIZER
# -----------------------------------------------
print("=" * 50)
print("STEP 7: Saving Model and Vectorizer")
print("=" * 50)

# Create models directory if it doesn't exist
models_dir = os.path.join(base_dir, "..", "models")
os.makedirs(models_dir, exist_ok=True)

# Save the trained model
model_path = os.path.join(models_dir, "model.pkl")
joblib.dump(model, model_path)
print(f"Model saved to: {model_path}")

# Save the fitted vectorizer
vectorizer_path = os.path.join(models_dir, "vectorizer.pkl")
joblib.dump(vectorizer, vectorizer_path)
print(f"Vectorizer saved to: {vectorizer_path}")

print("\n" + "=" * 50)
print("TRAINING COMPLETE!")
print("=" * 50)
print("Files created:")
print("  - models/model.pkl")
print("  - models/vectorizer.pkl")
print("\nYou can now use predict.py to make predictions.")
