# YouTube Comment Sentiment Analysis

This project performs sentiment analysis on YouTube video comments. By using the YouTube Data API to fetch comments and the VADER sentiment analysis tool from NLTK, the project analyzes the sentiment of the comments and provides insights into the overall sentiment (positive, neutral, or negative) of the comments on a video.

## Features

- Fetch comments from a YouTube video using the YouTube Data API.
- Analyze the sentiment of the fetched comments using VADER sentiment analysis.
- Display sentiment results including the count of positive, neutral, and negative comments.
- Visualize sentiment distribution using a pie chart.
- Simple and user-friendly web interface built with Flask, HTML, and Bootstrap.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, Bootstrap, JavaScript
- **Sentiment Analysis**: NLTK (VADER SentimentIntensityAnalyzer)
- **API**: Google YouTube Data API v3
- **Visualization**: Chart.js

## Prerequisites

Before running the project, ensure you have the following:

- Python 3.x
- Flask
- NLTK
- Google API Client
- YouTube Data API Key

## Setup Instructions

### Step 1: Clone the repository

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/YouTube-Comment-Sentiment-Analysis.git
cd YouTube-Comment-Sentiment-Analysis
