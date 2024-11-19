# web scrapper for reddit
import praw

# initialize Reddit API
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent=""
)

def scrape_subreddit(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit_name.hot(limit=limit):
        posts.append({"title": post.title, "selftext": post.selftext})
    return posts