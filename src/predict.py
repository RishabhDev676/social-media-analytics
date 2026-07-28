import pandas as pd
import joblib
import os
from preprocessing import preprocess_text


def load_model():
    """Load the trained model and vectorizer from the models folder."""

    # Get the path to the models folder
    # os.path.dirname(__file__) gives us the 'src' folder
    # Then we go up one level and into 'models'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "..", "models")

    model_path = os.path.join(models_dir, "model.pkl")
    vectorizer_path = os.path.join(models_dir, "vectorizer.pkl")

    # Check if model files exist
    if not os.path.exists(model_path):
        print("Error: model.pkl not found! Please run train_model.py first.")
        return None, None

    if not os.path.exists(vectorizer_path):
        print("Error: vectorizer.pkl not found! Please run train_model.py first.")
        return None, None

    # Load the model and vectorizer
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    print("Model and vectorizer loaded successfully!")
    return model, vectorizer


def predict_sentiment(text, model, vectorizer):
    """Predict the sentiment of a single comment.
    
    Steps:
    1. Preprocess the text (clean it)
    2. Convert text to numbers using the vectorizer
    3. Use the model to predict sentiment
    """

    # Step 1: Clean the text
    cleaned_text = preprocess_text(text)

    # Step 2: Convert to numerical features
    # We put it in a list because the vectorizer expects a list of texts
    text_features = vectorizer.transform([cleaned_text])

    # Step 3: Predict
    prediction = model.predict(text_features)

    return prediction[0]


def predict_from_csv(file_path, model, vectorizer):
    """Predict sentiments for all comments in a CSV file.
    
    The CSV should have a 'comment' column.
    Returns a DataFrame with original comment, cleaned comment, and predicted sentiment.
    """

    # Read the CSV
    df = pd.read_csv(file_path)

    # Check if 'comment' column exists
    if "comment" not in df.columns:
        print("Error: CSV must have a 'comment' column!")
        return None

    # Preprocess all comments
    df["cleaned_comment"] = df["comment"].apply(preprocess_text)

    # Convert all cleaned comments to numerical features
    text_features = vectorizer.transform(df["cleaned_comment"])

    # Predict sentiments for all comments
    df["sentiment"] = model.predict(text_features)

    # Keep only the useful columns
    result_df = df[["comment", "cleaned_comment", "sentiment"]]

    return result_df


# -----------------------------------------------
# This part runs only when you run this file directly
# -----------------------------------------------
if __name__ == "__main__":

    # Load the trained model
    model, vectorizer = load_model()

    if model is not None:
        # Test with a single comment
        test_comment = "I really enjoyed the movie, it was fantastic!"
        result = predict_sentiment(test_comment, model, vectorizer)
        print(f"\nComment: {test_comment}")
        print(f"Predicted Sentiment: {result}")

        # Test with another comment
        test_comment2 = "Terrible experience, worst product ever"
        result2 = predict_sentiment(test_comment2, model, vectorizer)
        print(f"\nComment: {test_comment2}")
        print(f"Predicted Sentiment: {result2}")
        
        # Predict sentiments for the test dataset and save to a new CSV
        base_dir = os.path.dirname(os.path.abspath(__file__))
        test_csv_path = os.path.join(base_dir, "..", "data", "test_100_comments.csv")
        output_csv_path = os.path.join(base_dir, "..", "data", "predicted_sentiments.csv")
        
        if os.path.exists(test_csv_path):
            print(f"\nPredicting sentiments for {test_csv_path}...")
            results_df = predict_from_csv(test_csv_path, model, vectorizer)
            if results_df is not None:
                results_df.to_csv(output_csv_path, index=False)
                print(f"Saved predicted sentiments to {output_csv_path}!")
                print("This file can now be used for statistical analysis and visualization.")
        else:
            print(f"\nCould not find {test_csv_path} to generate predictions.")

        