from dataclasses import dataclass
from typing import Optional, TypedDict
from datetime import datetime
from langchain.text_splitter import TokenTextSplitter
import asyncio
from langchain.prompts import PromptTemplate
from langchain.chains import load_summarize_chain

@dataclass
class RedditData:
    """Data for a summary."""
    title: str
    subreddit: str
    selftext: Optional[str] = None
    comments: Optional[str] = None
    query: str = f""
                
    def get_data_chunks(self) -> str:
        prompt = f"Title: {self.title}\nSubreddit: {self.subreddit}\n\n"
        if self.selftext:
            prompt += f"Post Text: {self.selftext}\n\n"
        if self.comments:
            prompt += f"<Comments subreddit='r/{self.subreddit}'>\n{self.comments}\n</Comments>\n"
        text_splitter = TokenTextSplitter(chunk_size=1024, chunk_overlap=100)
        prompt_docs = [Document(page_content=prompt)]
        prompt_chunks = text_splitter.split_documents(prompt_docs)
        return prompt_chunks

    async def get_summary(self, llm):
        prompt_template = """(Todays Date: """+datetime.now().strftime('%Y-%b-%d')+""") Revise and summarize"\
                " the article in 250 words or less by incorporating relevant information from the comments."\
                " Ensure the content is clear, engaging, and easy to understand for a"\
                " general audience. Avoid technical language, present facts objectively,"\
                " and summarize key comments from Reddit. Ensure that the overall"\
                " sentiment expressed in the comments is accurately reflected. Optimize"\
                " for highly original content. Don't be trolled by joke comments. Ensure"\
                " its written professionally, in a way that is appropriate for the"\
                " situation. Format the document using markdown and include links from the"\
                " original article/reddit thread.
        {text}
        CONCISE SUMMARY:"""
        prompt = PromptTemplate.from_template(prompt_template)

        refine_template = (
            "Your job is to produce a final summary\n"
            "We have provided an existing summary up to a certain point: {existing_answer}\n"
            "We have the opportunity to refine the existing summary"
            "(only if needed) with some more context below.\n"
            "------------\n"
            "{text}\n"
            "------------\n"
            "Given the new context, refine the original summary"
            "If the context isn't useful, return the original summary."
        )
        refine_prompt = PromptTemplate.from_template(refine_template)
        try:
            chain = load_summarize_chain(
                    llm=llm,
                    chain_type="refine",
                    question_prompt=prompt,
                    refine_prompt=refine_prompt,
                    return_intermediate_steps=True,
                    input_key="input_documents",
                    output_key="output_text",
                )
            result = await chain({"input_documents": self.get_data_chunks()}, return_only_outputs=True)
            return result["output_text"]
        except:
            print("Load a valid LLM")
            return ""
        