from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
import tiktoken

from judini.codegpt.agent import Agent
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()



app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}

class Item(BaseModel):
    text: str



@app.post("/prompt/")
def read_prompt(item:Item):
    prompt = item.text
    codegpt_api_key= os.getenv("CODEGPT_API_KEY")
    codegpt_agent_id= os.getenv("CODEGPT_AGENT_ID")

    agent_instance = Agent(api_key=codegpt_api_key, agent_id=codegpt_agent_id)

    # prompt = "tell me short story about blue turtle"

    response = asyncio.run(agent_instance.completion(prompt, stream=True))

    

    
    return response
    




@app.post("/check/")
async def create_item(item: Item):


    print(item)

    result = num_tokens_from_string(item.text, "cl100k_base")

    return result


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens



