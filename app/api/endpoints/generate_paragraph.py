from fastapi import APIRouter, HTTPException
from app.models.story_models import UserChoice
from app.services.story_generator import generate_next_paragraph, get_story_state

router = APIRouter()

@router.post("/")
async def generate_paragraph(user_choice: UserChoice):
    """
    Generate the next paragraphs based on the user's choice.
    """
    try:
        story_state = get_story_state(user_choice.story_id)
        
        paragraphs, choices = generate_next_paragraph(user_choice)
        
        return {
            "story_id": user_choice.story_id,
            "paragraphs": paragraphs,
            "choices": [{"text": choice.text, "meta_description": choice.meta_description} for choice in choices],
            "story_progress": story_state.story_progress
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))