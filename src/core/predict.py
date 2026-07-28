import pandas as pd
from src.core.preprocess import preprocess_text
from src.core.model_manager import ModelManager

# Initialize the ModelManager once at the module level
# This will allow it to cache the models effectively
manager = ModelManager()

def predict_text(text):
    """
    Predict the sentiment of a single comment string.
    
    Args:
        text (str): The comment to analyze.
        
    Returns:
        str: The predicted sentiment (e.g., 'Positive', 'Negative', 'Neutral').
    """
    model, vectorizer = manager.get_models()

    # Preprocess and vectorize
    cleaned_text = preprocess_text(text)
    text_features = vectorizer.transform([cleaned_text])

    # Predict
    prediction = model.predict(text_features)
    return prediction[0]

def predict_dataframe(df, text_column="comment"):
    """
    Predict sentiments for all comments in a pandas DataFrame.
    
    Args:
        df (pd.DataFrame): The dataframe containing the comments.
        text_column (str): The name of the column containing the text.
        
    Returns:
        pd.DataFrame: A dataframe containing the original comment, 
                      the cleaned comment, and the predicted sentiment.
    """
    if text_column not in df.columns:
        raise ValueError(f"DataFrame must have a '{text_column}' column!")

    model, vectorizer = manager.get_models()

    # Preprocess
    df["cleaned_comment"] = df[text_column].apply(preprocess_text)

    # Vectorize
    text_features = vectorizer.transform(df["cleaned_comment"])

    # Predict
    df["sentiment"] = model.predict(text_features)

    # Return only the essential columns for UI / Analytics
    result_df = df[[text_column, "cleaned_comment", "sentiment"]].copy()
    return result_df

if __name__ == "__main__":
    print("Testing Prediction Module...")
    
    # 1. Test single string
    comment = "I really love the new design, it's absolutely fantastic!"
    sentiment = predict_text(comment)
    print(f"\nComment: '{comment}'")
    print(f"Predicted: {sentiment}")
    
    # 2. Test DataFrame
    test_data = {
        "comment": [
            "Terrible customer service. Very disappointed.",
            "It's an okay product, nothing special.",
            "Amazing quality, will definitely buy again!"
        ]
    }
    test_df = pd.DataFrame(test_data)
    print("\nTesting DataFrame prediction...")
    predicted_df = predict_dataframe(test_df)
    
    print("\nResulting DataFrame:")
    print(predicted_df)
    
    # Notice how "Loading model..." is not printed multiple times because of the cache!