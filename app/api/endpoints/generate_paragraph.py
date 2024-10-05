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
        
        paragraphs, choice1, choice2 = generate_next_paragraph(user_choice)
        
        return {
            "story_id": user_choice.story_id,
            "paragraphs": paragraphs,
            "choice1": {
                "text": choice1.text,
                "meta_caption": choice1.meta_caption
            },
            "choice2": {
                "text": choice2.text,
                "meta_caption": choice2.meta_caption
            },
            "paragraphs_count": len(story_state.paragraphs)
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))