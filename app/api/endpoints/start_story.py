from fastapi import APIRouter
from app.models.story_models import StartStoryInput, UserChoice
from app.services.story_generator import generate_next_paragraph, create_story
import uuid

router = APIRouter()

@router.post("/")
async def start_story(input_data: StartStoryInput):
    """
    Initialize the story and return the first paragraph along with choices.
    """
    story_id = str(uuid.uuid4())
    
    create_story(
        story_id=story_id,
        genre=input_data.genre,
        genre_description=input_data.genre_description,
        location=input_data.location,
        location_description=input_data.location_description,
        main_character_name=input_data.main_character_name,
        main_character_description=input_data.main_character_description
    )
    
    initial_choice = UserChoice(
        story_id=story_id, 
        choice=f"Start a {input_data.genre} story with {input_data.main_character_name}"
    )
    
    paragraph, choices = generate_next_paragraph(initial_choice)
    
    return {
        "story_id": story_id,
        "paragraph": paragraph,
        "choices": [{"text": choice.text, "meta_description": choice.meta_description} for choice in choices]
    }
