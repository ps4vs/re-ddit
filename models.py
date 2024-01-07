from datatypes import RedditData
from typing import Any
from utils import get_comments, createLLM, createTTS, createSTT

class Model():
    def __init__(self):
        self.LLM = createLLM()
        self.TTS = createTTS()
        self.STT = createSTT()
    
    async def summarize(self, post):
        print("summarise start")
        print(f"Title is {post.title}")
        print(post.selftext)
        ### summarise the comments tree.
        post.comment_sort = "top"
        comments = await post.comments()
        await comments.replace_more(limit=None)
        comment_string = ""
        for comment in comments:
            comment_string+=get_comments(comment)
            
        data = RedditData(post.title, post.subreddit, post.selftext, comment_string)
        summary = await data.get_summary(self.LLM)
        print(summary)
        print("summarise done")
        return post.title
    
    async def speak(self, content):
        print("speak started")
        print(f"content is {content}")
        print("speak done")
        return
        
    async def listen(self):
        ### TODO
        return
    