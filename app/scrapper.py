import praw
from dotenv import load_dotenv
from transformers import pipeline
import os
import json

# Web scrapper for reddit

# Load environment variables from .env
load_dotenv()

# Initialize Reddit API
reddit = praw.Reddit(
    client_id = os.getenv("CLIENT_ID"),
    client_secret = os.getenv("CLIENT_SECRET"),
    user_agent = os.getenv("USER_AGENT")
)

def scrape_subreddit(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.hot(limit=limit):
        posts.append({"title": post.title, "selftext": post.selftext})
    return posts

# Load Hugging Face sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(posts):
    for post in posts:
        sentiment = sentiment_analyzer(post["selftext"][:500]) # Limit text to 500 characters
        post["sentiment"] = sentiment[0]
    return posts

if __name__ == "__main__":
    # Prompt the user for a subreddit name
    subreddit_name = input ("enter the name of a subreddit to scrape (e.g., python)")

    try:
        # Scrape the subreddit
        posts = scrape_subreddit(subreddit_name, limit=5)
        posts = analyze_sentiment(posts)

        # Print the results
        print(f"Top posts from r/{subreddit_name}:")
        for i, post in enumerate(posts, start=1):
            print(f"{i}. {post['title']}")
            print(f"    {post['selftext'][:200]}...") # Display the first 200 characters of the text
            print()
        
        # Save posts to a JSON file
        with open(f"{subreddit_name}_posts.json", "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=4)
        print(f"Saved posts to {subreddit_name}_posts.json")
    except Exception as e:
        print(f"An error occurred: {e}")


