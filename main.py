from redditAPI import Reddit
from models import Model
import asyncio

async def process_post(key, reddit, model):
    try:
        # Assuming this is an async generator
        async for curr_post in reddit.queryXsubreddit_dic[key]:
            summary = await model.summarize(curr_post)
            if summary:  # Check if there is a summary
                await model.speak(summary)
    except StopAsyncIteration:
        print(f"Finished processing posts for {key}")
        
async def async_main():
    reddit = Reddit()
    model = Model()
    
    query = "open source LLM for functional calls"
    subreddits = ["LocalLlama"]
    
    await reddit.create_queryXsubreddit(query, subreddits)
    keys = [(query, subreddits[0])]
    tasks = [process_post(k, reddit, model) for k in keys]
    await asyncio.gather(*tasks)
    await reddit.close()

if __name__=="__main__":
    asyncio.run(async_main())