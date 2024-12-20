from googleapiclient.discovery import build
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
    sentiment_results = []
    
    for comment in comments:
        sentiment_score = analyzer.polarity_scores(comment)
        sentiment_results.append({
            'comment': comment,
            'sentiment': sentiment_score
        })
    
    return sentiment_results

# Example usage
video_url = 'https://www.youtube.com/watch?v=FqfoDUhzyDo&ab_channel=TrainWithShubham'
comments = get_comments(video_url)
print("Comments:", comments)

# Analyze sentiment of the comments
sentiment_analysis = analyze_sentiment(comments)

# Print the sentiment analysis results
for result in sentiment_analysis:
    print(f"Comment: {result['comment']}")
    print(f"Sentiment Scores: {result['sentiment']}")
    print("------")
