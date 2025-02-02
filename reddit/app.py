import os
import praw
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from typing import List
load_dotenv(".env")

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
USER_AGENT = os.environ["USER_AGENT"]

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

print("Connection status : ", reddit.read_only)

# Initialize FastAPI app
app = FastAPI(title="Reddit Posts API")

@app.get("/posts", summary="Extract posts from a set of subreddits")
def get_posts(subreddits: List[str] = Query(..., description="List of subreddit names"), limit: int = 10):
    """
    Extract posts from a list of subreddits.
    
    Query Parameters:
      - subreddits: List of subreddit names (e.g., subreddits=python&subreddits=learnprogramming)
      - limit: Number of posts to retrieve per subreddit (default: 10)
    
    Returns:
      A dict mapping each subreddit name to a list of posts with their id, title, and url.
    """
    result = {}
    for sub in subreddits:
        try:
            subreddit_instance = reddit.subreddit(sub)
            posts = []
            for post in subreddit_instance.hot(limit=limit):
                posts.append({
                    "id": post.id,
                    "title": post.title,
                    "url": post.url
                })
            result[sub] = posts
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error retrieving posts from subreddit '{sub}': {str(e)}")
    return result

@app.get("/post/{post_id}", summary="Extract content of a post")
def get_post_content(post_id: str):
    """
    Extract and return the content of a post given its id.
    
    Path Parameters:
      - post_id: The Reddit post id.
    
    Returns:
      A dict containing the post's id, title, selftext, and url.
    """
    try:
        submission = reddit.submission(id=post_id)
        # Ensure the submission data is loaded
        submission.comments.replace_more(limit=0)
        return {
            "id": submission.id,
            "title": submission.title,
            "selftext": submission.selftext,
            "url": submission.url
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving post with id '{post_id}': {str(e)}")

@app.get("/")
async def root():
    return {"message": "Reddit API Server is running!"}

