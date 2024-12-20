from googleapiclient.discovery import build
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

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
    
    for comment in comments:
        sentiment_score = analyzer.polarity_scores(comment)
        compound_score = sentiment_score['compound']
        
        # Classify the sentiment based on the compound score
        if compound_score >= 0.05:
            sentiment_results['positive'] += 1
        elif compound_score <= -0.05:
            sentiment_results['negative'] += 1
        else:
            sentiment_results['neutral'] += 1
    
    return sentiment_results

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

# Example usage
video_url = 'https://www.youtube.com/watch?v=FqfoDUhzyDo&ab_channel=TrainWithShubham'
comments = get_comments(video_url)

# Analyze sentiment of the comments
sentiment_analysis = analyze_sentiment(comments)

# Print the sentiment analysis results
for result in sentiment_analysis:
    print(f"{result}: {sentiment_analysis[result]} comments")

# Visualize the sentiment distribution
visualize_sentiment(sentiment_analysis)
