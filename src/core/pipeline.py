import pandas as pd
from src.core.predict import predict_dataframe
from src.analytics.statistics import compute_statistics, compute_text_statistics, compute_frequency_table

def run_analysis_pipeline(file_path, text_column="comment"):
    """
    End-to-end pipeline to process a CSV file, predict sentiments, 
    and calculate all necessary statistics.
    
    Args:
        file_path (str): The absolute or relative path to the CSV file.
        text_column (str): The column containing comments.
        
    Returns:
        dict: A dictionary containing:
            - "data": The enriched pd.DataFrame (with predicted sentiments).
            - "stats": Summary statistics dictionary.
            - "text_stats": Text length statistics dictionary.
            - "freq_table": Frequency distribution pd.DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise IOError(f"Could not read CSV file at {file_path}: {e}")
        
    if text_column not in df.columns:
        raise ValueError(f"CSV must contain a '{text_column}' column.")

    # 1. Predict Sentiments
    enriched_df = predict_dataframe(df, text_column=text_column)
    
    # 2. Compute Statistics
    stats = compute_statistics(enriched_df)
    text_stats = compute_text_statistics(enriched_df, column_name=text_column)
    freq_table = compute_frequency_table(enriched_df)
    
    # 3. Bundle Results
    return {
        "data": enriched_df,
        "stats": stats,
        "text_stats": text_stats,
        "freq_table": freq_table
    }

if __name__ == "__main__":
    import os
    print("Testing Pipeline...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_csv = os.path.join(base_dir, "..", "..", "data", "uploaded", "test_100_comments.csv")
    
    if os.path.exists(test_csv):
        results = run_analysis_pipeline(test_csv)
        print("\nPipeline execution successful!")
        print(f"Total Comments Processed: {results['stats']['total']}")
        print(f"Dominant Sentiment: {results['stats']['dominant_sentiment']}")
        print("\nFrequency Table:")
        print(results['freq_table'])
    else:
        print(f"Could not find test CSV at {test_csv}")
