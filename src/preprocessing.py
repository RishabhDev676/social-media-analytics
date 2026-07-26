import re
import nltk
from nltk.corpus import stopwords

# Download stopwords if not already downloaded
nltk.download("stopwords", quiet=True)

# Load English stop words
stop_words = set(stopwords.words("english"))


def preprocess_text(text):
    """Clean a single text comment.
    
    Steps:
    1. Convert to string (handles any non-string values)
    2. Convert to lowercase
    3. Remove URLs
    4. Remove punctuation, numbers, and special characters
    5. Remove stop words
    6. Remove extra spaces
    
    Example:
        Input:  "I absolutely LOVE this product!!! Visit https://abc.com"
        Output: "absolutely love product"
    """

    # Step 1: Convert to string
    text = str(text)

    # Step 2: Convert to lowercase
    text = text.lower()

    # Step 3: Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # Step 4: Remove punctuation, numbers, and special characters
    # Keep only letters and spaces
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Step 5: Remove stop words
    words = text.split()
    words = [word for word in words if word not in stop_words]

    # Step 6: Join words and remove extra spaces
    text = " ".join(words)

    return text


def preprocess_dataframe(df, column="comment"):
    """Apply preprocessing to an entire DataFrame column.
    
    Takes a DataFrame and the name of the column containing comments.
    Adds a new column called 'cleaned_comment' with the cleaned text.
    Returns the updated DataFrame.
    """

    df["cleaned_comment"] = df[column].apply(preprocess_text)
    return df


# -----------------------------------------------
# This part runs only when you run this file directly
# -----------------------------------------------
if __name__ == "__main__":
    # Quick test
    test_text = "I absolutely LOVE this product!!! Visit https://abc.com #best @user123"
    result = preprocess_text(test_text)
    print(f"Original: {test_text}")
    print(f"Cleaned:  {result}")
