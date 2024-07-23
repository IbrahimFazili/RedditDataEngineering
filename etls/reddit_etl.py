from praw import Reddit
import sys
import pandas as pd
import numpy as np
from utils.constants import POST_FIELDS

def connect_reddit(client_id, client_secret, user_agent) -> Reddit:
    try:
        reddit = Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        print("Connected to Reddit!")
        return reddit
    except Exception as e:
        print("Cannot connect to Reddit. Error: ", e)
        sys.exit(1)


def extract_posts(reddit_instance: Reddit, subreddit: str, time_filter='day', limit=None):
    # fetch the subreddit
    subreddit = reddit_instance.subreddit(subreddit)

    # fetch the posts
    posts = subreddit.top(time_filter=time_filter, limit=limit)

    post_lists = []

    for post in posts:
        # post_dict returns the post information as a dictionary
        post_dict = vars(post)

        # extracts the required information by looking at the field
        post = {key: post_dict[key] for key in POST_FIELDS}
        
        post_lists.append(post)

    return post_lists

def transform_data(post_df: pd.DataFrame):
    post_df['created_utc'] = pd.to_datetime(post_df['created_utc'], unit='s')
    post_df['over_18'] = np.where(post_df['over_18'] == True, True, False)
    post_df['author'] = post_df['author'].astype(str)

    return post_df

def load_data_to_csv(post_df: pd.DataFrame, file_name: str):
    post_df.to_csv(file_name, index=False)