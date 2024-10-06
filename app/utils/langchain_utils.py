from app.core.config import settings
import os
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from app.utils.story_progression import get_story_context

class Choice(BaseModel):
    text: str
    meta_description: str

class StoryContent(BaseModel):
    paragraphs: List[str]
    choices: List[Choice]

def get_openai_client():
    api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in environment variables or .env file")
    return OpenAI(api_key=api_key)

def get_story_prompt():
    return """
    You are a comic book storyteller crafting an interactive {genre} comic: {genre_description} 
    The main character is named {main_character_name}, described as: {main_character_description}
    The location is {location}, described as: {location_description}

    Story Structure Context:
    {story_context}

    Based on the following context and user's choice, continue the story:

    Previous Context: {context}
    User's Choice: {user_choice}

    Generate the next part of the story as a list of 3 short paragraphs of 30 words each and provide two new choices for the user.
    Each paragraph in the list should be a self-contained unit of the story, without any dialogs.
    Assume that your audience is an 8th grader. Your vocabulary must be simple and your language must be clear and easy to understand.
    
    Ensure that the story adheres to the {genre} genre, maintains consistency with the main character, and follows the hero's journey template.
    Consider both the current stage and the upcoming stage when crafting the story and choices.

    For the choices:
    1. Create two distinctly different paths for the story to branch into.
    2. The choices should present a clear contrast, such as:
       - Moral dilemmas (e.g., sacrifice vs. self-preservation)
       - Strategic decisions (e.g., stealth vs. direct confrontation)
       - Character development (e.g., trust vs. suspicion)
       - Plot direction (e.g., explore a new area vs. confront the antagonist)
    3. Ensure that each choice would lead to significantly different outcomes or story directions.
    4. The choices should be impactful and have clear consequences for the character or story.

    Respond with a JSON object containing:
    1. A 'paragraphs' field with a list of 3 paragraph strings for the story content.
    2. A 'choices' array with two objects, each having:
       - 'text' (about 5-10 words) for the user-facing choice
       - 'meta_description' (about 15 words) for image generation input
    
    Make sure the choices are meaningful, contrasting, and will lead the story towards distinctly different paths.
    """

def generate_story_content(
    genre: str,
    genre_description: str,
    main_character_name: str,
    main_character_description: str,
    context: str,
    user_choice: str,
    location: str,
    location_description: str,
    story_progress: int
) -> StoryContent:
    client = get_openai_client()
    prompt = get_story_prompt()
    story_context = get_story_context(story_progress)
    
    messages = [
        {"role": "system", "content": "You are a comic book storyteller. Generate story content based on the given parameters."},
        {"role": "user", "content": prompt.format(
            genre=genre,
            genre_description=genre_description,
            main_character_name=main_character_name,
            main_character_description=main_character_description,
            context=context,
            user_choice=user_choice,
            location=location,
            location_description=location_description,
            story_context=story_context
        )}
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.7
    )

    response_content = completion.choices[0].message.content
    story_content = StoryContent.model_validate_json(response_content)
    return story_content
