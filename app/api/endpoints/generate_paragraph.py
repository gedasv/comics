from fastapi import APIRouter, HTTPException
from app.models.story_models import UserChoice
from app.services.story_generator import generate_next_paragraph, get_story_state

router = APIRouter()

@router.post("/")
async def generate_paragraph(user_choice: UserChoice):
    """
    Generate the next paragraph based on the user's choice.
    """
    try:
        story_state = get_story_state(user_choice.story_id)
        
        paragraph, choices = generate_next_paragraph(user_choice)
        
        return {
            "story_id": user_choice.story_id,
            "paragraph": paragraph,
            "choices": [{"text": choice.text, "meta_description": choice.meta_description} for choice in choices],
            "paragraphs_count": len(story_state.paragraphs)
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))