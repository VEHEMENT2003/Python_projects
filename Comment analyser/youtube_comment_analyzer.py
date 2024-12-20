from googleapiclient.discovery import build
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import json

# Set up your API key
API_KEY = 'AIzaSyDs5-8hZI486r5ftzNUs-RGTroHjwhoIEU'

# Download necessary NLTK data
nltk.download('vader_lexicon')

# Function to get video ID from YouTube URL
def get_video_id(url):
    video_id = url.split('v=')[1].split('&')[0]
    return video_id

# Function to get comments from YouTube video
def get_comments(video_url):
    video_id = get_video_id(video_url)
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100  # Max number of comments per request
    )
    response = request.execute()
    
    # Extract comments
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    
    return comments

# Function to analyze sentiment of a comment
def analyze_sentiment(comments):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_results = {'positive': 0, 'neutral': 0, 'negative': 0}
    compound_scores = []  # To calculate average sentiment score
    
    for comment in comments:
        sentiment_score = analyzer.polarity_scores(comment)
        compound_score = sentiment_score['compound']
        compound_scores.append(compound_score)
        
        # Classify the sentiment based on the compound score
        if compound_score >= 0.05:
            sentiment_results['positive'] += 1
        elif compound_score <= -0.05:
            sentiment_results['negative'] += 1
        else:
            sentiment_results['neutral'] += 1
    
    # Calculate average compound score for the video
    avg_sentiment_score = sum(compound_scores) / len(compound_scores) if compound_scores else 0
    
    return sentiment_results, avg_sentiment_score

# Function to visualize the sentiment distribution
def visualize_sentiment(sentiment_results):
    # Data for visualization
    sentiments = list(sentiment_results.keys())
    counts = list(sentiment_results.values())
    
    # Plotting the bar chart
    plt.figure(figsize=(8, 6))
    sns.barplot(x=sentiments, y=counts, palette="viridis")
    plt.title("Sentiment Distribution of YouTube Comments")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Comments")
    plt.show()

# Function to store sentiment results in CSV
def store_results_csv(sentiment_results, avg_sentiment_score, filename='sentiment_results.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sentiment', 'Count'])
        for sentiment, count in sentiment_results.items():
            writer.writerow([sentiment, count])
        writer.writerow(['Average Sentiment Score', avg_sentiment_score])

# Function to store sentiment results in JSON
def store_results_json(sentiment_results, avg_sentiment_score, filename='sentiment_results.json'):
    results = {
        'sentiment_distribution': sentiment_results,
        'average_sentiment_score': avg_sentiment_score
    }
    with open(filename, 'w') as json_file:
        json.dump(results, json_file, indent=4)

# Example usage
video_url = 'https://www.youtube.com/watch?v=FqfoDUhzyDo&ab_channel=TrainWithShubham'
comments = get_comments(video_url)

# Analyze sentiment of the comments
sentiment_analysis, avg_sentiment_score = analyze_sentiment(comments)

# Print the sentiment analysis results
for result in sentiment_analysis:
    print(f"{result}: {sentiment_analysis[result]} comments")

# Visualize the sentiment distribution
visualize_sentiment(sentiment_analysis)

# Store the results in CSV and JSON formats
store_results_csv(sentiment_analysis, avg_sentiment_score)
store_results_json(sentiment_analysis, avg_sentiment_score)

