import numpy as np
import pandas as pd
import os

def compute_statistics(df):
    """Calculate comprehensive summary statistics from sentiment predictions.

    Input: DataFrame with a 'sentiment' column
    Output: Dictionary with total counts, percentages, and advanced metrics
    """
    if df is None or df.empty or "sentiment" not in df.columns:
        return {}

    total = len(df)

    # Count each sentiment
    counts = df["sentiment"].value_counts()
    positive_count = int(counts.get("Positive", 0))
    negative_count = int(counts.get("Negative", 0))
    neutral_count = int(counts.get("Neutral", 0))

    # Calculate percentages
    positive_pct = float(round((positive_count / total) * 100, 2)) if total > 0 else 0.0
    negative_pct = float(round((negative_count / total) * 100, 2)) if total > 0 else 0.0
    neutral_pct = float(round((neutral_count / total) * 100, 2)) if total > 0 else 0.0

    # Calculate Sentiment Index (-1 to +1 scale)
    # (+1 * Pos + 0 * Neu + -1 * Neg) / Total
    sentiment_index = float(
        round((positive_count - negative_count) / total, 2)
    ) if total > 0 else 0.0

    # Determine Dominant Sentiment
    sentiment_map = {
        "Positive": positive_count,
        "Negative": negative_count,
        "Neutral": neutral_count,
    }
    dominant_sentiment = max(sentiment_map, key=sentiment_map.get) if total > 0 else "None"

    stats = {
        "total": total,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "neutral_count": neutral_count,
        "positive_pct": positive_pct,
        "negative_pct": negative_pct,
        "neutral_pct": neutral_pct,
        "sentiment_index": sentiment_index,
        "dominant_sentiment": dominant_sentiment,
    }
    return stats


def compute_text_statistics(df, column_name="comment"):
    """Calculate text length statistics (Mean, Median, Std Dev) for UI displays."""
    if df is None or df.empty or column_name not in df.columns:
        return {}

    lengths = df[column_name].astype(str).apply(len)

    return {
        "avg_length": float(round(lengths.mean(), 2)),
        "median_length": float(round(lengths.median(), 2)),
        "std_length": float(round(lengths.std(), 2)),
        "max_length": int(lengths.max()),
        "min_length": int(lengths.min()),
    }


def compute_frequency_table(df):
    """Generate a frequency distribution table for sentiments."""
    if df is None or df.empty or "sentiment" not in df.columns:
        return pd.DataFrame()

    freq = df["sentiment"].value_counts().reset_index()
    freq.columns = ["Sentiment", "Frequency"]

    total = len(df)
    freq["Percentage (%)"] = round((freq["Frequency"] / total) * 100, 2) if total > 0 else 0.0
    freq["Cumulative Frequency"] = freq["Frequency"].cumsum()

    return freq


# Test block
if __name__ == "__main__":
    from src.core.predict import predict_dataframe
    
    print("Testing Statistics Module with actual predictions...")
    
    # Load test dataset
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_csv_path = os.path.join(base_dir, "..", "..", "data", "uploaded", "test_100_comments.csv")
    
    if os.path.exists(test_csv_path):
        test_df = pd.read_csv(test_csv_path)
        predicted_df = predict_dataframe(test_df)
        
        print("\n--- Summary Statistics ---")
        print(compute_statistics(predicted_df))

        print("\n--- Text Statistics ---")
        print(compute_text_statistics(predicted_df))

        print("\n--- Frequency Table ---")
        print(compute_frequency_table(predicted_df))
    else:
        print(f"Could not find {test_csv_path} to test statistics.")