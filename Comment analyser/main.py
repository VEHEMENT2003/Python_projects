from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

app = Flask(__name__)

# Set up your API key securely using environment variables
API_KEY = os.getenv('YOUTUBE_API_KEY')  # Ensure you set this in your environment

# Function to get video ID from YouTube URL
def get_video_id(url):
    try:
        video_id = url.split('v=')[1].split('&')[0]
        return video_id
    except IndexError:
        raise ValueError("Invalid YouTube URL")

# Function to get comments from YouTube video
def get_comments(video_url):
    video_id = get_video_id(video_url)
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    comments = []
    try:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100
        )
        response = request.execute()
        
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        
        return comments
    except Exception as e:
        raise Exception(f"Error fetching comments: {str(e)}")

# Function to analyze sentiment of comments
def analyze_sentiment(comments):
    analyzer = SentimentIntensityAnalyzer()
    positive, neutral, negative = 0, 0, 0

    for comment in comments:
        sentiment_score = analyzer.polarity_scores(comment)
        compound_score = sentiment_score['compound']

        if compound_score >= 0.05:
            positive += 1
        elif compound_score <= -0.05:
            negative += 1
        else:
            neutral += 1

    total_comments = len(comments)
    sentiment_data = {
        'positive': positive,
        'neutral': neutral,
        'negative': negative,
        'avg_sentiment_score': (positive - negative) / total_comments if total_comments else 0
    }
    return sentiment_data

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    video_url = data.get('videoUrl')

    if not video_url:
        return jsonify({"error": "Video URL is required"}), 400
    
    try:
        # Fetch comments and analyze sentiment
        comments = get_comments(video_url)
        sentiment_data = analyze_sentiment(comments)
        return jsonify(sentiment_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
