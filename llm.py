import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Literal

from config import OPENAI_API_KEY, LLM_MODEL
from prompts import get_system_prompt

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

# 1. configure the openai client with the 'instructor' patch
client = instructor.patch(OpenAI(api_key=OPENAI_API_KEY))


class SpeakerDeliberation(BaseModel):
    thoughts: str = Field(..., description="Your private thoughts and reasoning for this round.")
    speech: str = Field(..., description="Your statement to the committee for this round.")
    vote: Literal["A", "B", "Undecided"]

class ListenerResponse(BaseModel):
    thoughts: str = Field(..., description="Your private reaction and thoughts on the speaker's statement.")
    vote: Literal["A", "B", "Undecided"]

class Reflection(BaseModel):
    thoughts: str = Field(..., description="Your private reflections and thoughts on the eviction event.")

class CorruptedSpeech(BaseModel):
    rewritten_speech: str = Field(..., description="The corrupted version of the original speech.")


def get_llm_response(prompt: str, response_model) -> BaseModel:
    """
    Generalized LLM call that accepts any Pydantic response_model.
    """
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            response_model=response_model,
            messages=[
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": prompt},
            ],
            temperature=1,
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        # Return a default object if the API call fails
        if response_model == SpeakerDeliberation:
            return response_model(thoughts="Error processing.", vote="Undecided", speech="Error.")
        elif response_model == ListenerResponse:
            return response_model(thoughts="Error processing.", vote="Undecided")
        elif response_model == Reflection:
            return response_model(thoughts="Error processing.")
        elif response_model == CorruptedSpeech:
            return response_model(rewritten_speech="Error processing.")
        else:
            return response_model(thoughts="Error processing.")