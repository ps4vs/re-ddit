from datetime import datetime
from typing import Any 
from llm_vm.client import Client

def get_comments(comment: Any, level: int = 0) -> str:
    """Get the comments from a Reddit thread."""
    result = ""
    author_name = comment.author.name if comment.author else "[deleted]"
    
    def format_date(timestamp: float) -> str:
        """Format a timestamp into a human-readable date."""
        date: datetime = datetime.fromtimestamp(timestamp)
        return date.strftime("%Y-%b-%d %H:%M")
    
    created_date = format_date(comment.created_utc)
    result += f"{created_date} [{author_name}] {comment.body}\n"
    for reply in sorted(
        comment.replies, key=lambda reply: reply.created_utc, reverse=True
    ):
        result += "    " * level
        result += "> " + get_comments(reply, level + 1)
    return result


def createLLM():
    client = Client(
        big_model='neo', 
        big_model_config={'model_uri':'EleutherAI/gpt-neo-2.7B'})
    #    big_model = 'neo',
    #    big_model_config={'model_uri':'EleutherAI/gpt-neox-20b'}, 
    #    small_model ='neo',
    #    small_model_config={'model_uri':'EleutherAI/gpt-neo-125m'})
    return client.complete

def createTTS():
    return "tts"

def createSTT():
    return "stt"

if __name__ == "__main__":
    llm = createLLM()
    print(llm("What is Anarchy?"))