import asyncpraw
import json
import asyncio 

class Reddit():
    def __init__(self):
        with open('client_secrets.json') as f:
            login_info = json.load(f)
        self.reddit = asyncpraw.Reddit(
            client_id=login_info['client_id'],
            client_secret=login_info['client_secret'],
            user_agent=login_info['user_agent'],
            redirect_uri=login_info['redirect_uri'],
            refresh_token=login_info['refresh_token'],
            # username=login_info['user'],
            # password=login_info['password']
        )
        self.queryXsubreddit_dic = {}
        
    async def create_queryXsubreddit(self, query, subreddits=["MachineLearning"], duration="month", sort="top", limit=5):
        
        async def get_relevant_posts_from_subreddit(query, subreddits=["MachineLearning"], duration="month", sort="top", limit=5):
            """Return generator to all the posts matching the given query from the given subreddits

            Args:
                query (str): query string which we want to search
                subreddits (list, optional): list of subreddit names which we want to search in. Defaults to ["MachineLearning"].
                duration (str, optional): duration from which the relevant posts should be extracted. Defaults to "month".
                sort (str, optional): way to sort these subreddits. Defaults to "top".

            Returns:
                generator: generator object to the posts, each post is a submission class type.
            """
            curr_subreddit = await self.reddit.subreddit(subreddits[0])
            async for submission in curr_subreddit.search(query=query, sort=sort, time_filter=duration, limit=limit):
                yield submission
        
        self.queryXsubreddit_dic[(query, subreddits[0])] = get_relevant_posts_from_subreddit(query, subreddits, duration, sort, limit)
        return
    
    async def close(self):
        await self.reddit.close()
        return


