import pandas as pd
import re
import nltk
from textblob import TextBlob
from nltk.corpus import stopwords

# Read CSV file
df = pd.read_csv("data.csv")

# Function to classify sentiment
def get_sentiment(comment):
    polarity = TextBlob(str(comment)).sentiment.polarity

    if polarity > 0.3:
        return "Positive"
    elif polarity < -0.3:
        return "Negative"
    else:
        return "Neutral"

stop_words = set(stopwords.words("english"))

def preprocess_text(text):

    # Convert to string
    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # Remove punctuation and special characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Split text into words
    words = text.split()

    # Remove stop words
    words = [word for word in words if word not in stop_words]

    # Join words back together
    text = " ".join(words)

    return text


# Apply preprocessing
df["sentiment"] = df["comment"].apply(get_sentiment)

df["cleaned_comment"] = df["comment"].apply(preprocess_text)

# -----------------------------
# STEP 3: SAVE FINAL DATASET
# -----------------------------
df = df[["comment", "cleaned_comment", "sentiment"]]
df.to_csv("final_processed_comments.csv", index=False)


# Display final dataset
print(df)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", 200)

print("\nFINAL PROCESSED DATASET:\n")
print(df.to_string(index=False))