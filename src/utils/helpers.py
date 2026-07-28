import csv
import random
import os

# Define components for sentence generation
positive_adjectives = ['amazing', 'excellent', 'fantastic', 'wonderful', 'great', 'awesome', 'brilliant', 'superb', 'perfect', 'stellar']
negative_adjectives = ['terrible', 'awful', 'horrible', 'worst', 'bad', 'disappointing', 'poor', 'dreadful', 'subpar', 'useless']
neutral_adjectives = ['okay', 'average', 'fine', 'acceptable', 'standard', 'typical', 'mediocre', 'normal', 'fair', 'regular']

subjects = ['The product', 'This item', 'The service', 'Delivery', 'Customer support', 'The quality', 'My experience', 'The price', 'The packaging', 'The design']
verbs_pos = ['is', 'looks', 'feels', 'seems', 'proved to be', 'was']
verbs_neg = ['is', 'looks', 'feels', 'seems', 'proved to be', 'was']
verbs_neu = ['is', 'looks', 'feels', 'seems', 'proved to be', 'was']

adverbs = ['really', 'absolutely', 'truly', 'quite', 'very', 'extremely', 'somewhat', 'fairly', 'totally', 'completely']

endings_pos = ['Highly recommended!', 'I love it.', 'Best purchase ever.', 'Will buy again.', 'Exceeded expectations.', 'Very satisfied.']
endings_neg = ['Total waste of money.', 'Do not buy.', 'I hate it.', 'Will return it.', 'Very frustrated.', 'Save your money.']
endings_neu = ['Nothing special.', 'It does the job.', 'As expected.', 'Might buy again.', 'Not bad, not great.', 'Serves its purpose.']

def generate_sentence(sentiment):
    subject = random.choice(subjects)
    adverb = random.choice(adverbs)
    
    if sentiment == 'Positive':
        verb = random.choice(verbs_pos)
        adj = random.choice(positive_adjectives)
        ending = random.choice(endings_pos)
    elif sentiment == 'Negative':
        verb = random.choice(verbs_neg)
        adj = random.choice(negative_adjectives)
        ending = random.choice(endings_neg)
    else:  # Neutral
        verb = random.choice(verbs_neu)
        adj = random.choice(neutral_adjectives)
        ending = random.choice(endings_neu)
        
    structure = random.choice([1, 2, 3])
    
    if structure == 1:
        sentence = f"{subject} {verb} {adj}. {ending}"
    elif structure == 2:
        sentence = f"{subject} {verb} {adverb} {adj}. {ending}"
    else:
        sentence = f"I think {subject.lower()} {verb} {adj}. {ending}"
        
    return sentence

def generate_dataset(num_comments=11000):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_csv_labels = os.path.join(base_dir, "..", "..", "data", "raw", "comments.csv")
    output_csv_no_labels = os.path.join(base_dir, "..", "..", "data", "raw", "data.csv")
    
    sentiments = ['Positive', 'Negative', 'Neutral']
    weights = [0.4, 0.4, 0.2]  # 40% pos, 40% neg, 20% neu
    
    print(f"Generating {num_comments} comments...")
    
    with open(output_csv_labels, 'w', newline='', encoding='utf-8') as f_labels, \
         open(output_csv_no_labels, 'w', newline='', encoding='utf-8') as f_no_labels:
         
        writer_labels = csv.writer(f_labels)
        writer_labels.writerow(['ID', 'comment', 'sentiment'])
        
        writer_no_labels = csv.writer(f_no_labels)
        writer_no_labels.writerow(['comment'])
        
        for i in range(1, num_comments + 1):
            true_sentiment = random.choices(sentiments, weights=weights)[0]
            comment = generate_sentence(true_sentiment)
            
            # Introduce 5% label noise to drop model accuracy to ~95%
            recorded_sentiment = true_sentiment
            if random.random() < 0.05:
                other_sentiments = [s for s in sentiments if s != true_sentiment]
                recorded_sentiment = random.choice(other_sentiments)
                
            writer_labels.writerow([i, comment, recorded_sentiment])
            writer_no_labels.writerow([comment])
            
    print(f"Successfully generated {num_comments} comments with ~5% label noise to '{output_csv_labels}'.")
    print(f"Also saved {num_comments} comments (text only) to '{output_csv_no_labels}'.")

if __name__ == "__main__":
    generate_dataset()
