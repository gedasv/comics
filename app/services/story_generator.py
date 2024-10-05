from app.models.story_models import UserChoice, StoryState
from app.utils.langchain_utils import generate_story_content
from fastapi import HTTPException

# In-memory storage for story states (replace with database later)
story_states: dict[str, StoryState] = {}

def generate_next_paragraph(user_choice: UserChoice):
    """
    Generate the next paragraph and choices based on the user's input.
    """
    story_id = user_choice.story_id
    story_state = story_states.get(story_id)

    if not story_state:
        raise HTTPException(status_code=404, detail="Story not found")

    context = "\n".join(story_state.paragraphs)
    
    result = generate_story_content(
        story_state.genre,
        story_state.genre_description,
        story_state.main_character_name,
        story_state.main_character_description,
        context,
        user_choice.choice,
        story_state.location,
        story_state.location_description,
        story_state.story_progress
    )
    
    # Update the story state
    story_state.paragraphs.append(result.paragraph)
    story_state.choices = [choice.text for choice in result.choices]
    story_state.current_state = result.paragraph
    story_state.story_progress += 1
    
    # TODO: Implement a more sophisticated ending condition
    if story_state.story_progress >= 10:
        story_state.choices = ["End the story", "End the story"]
    
    return result.paragraph, story_state.choices

def get_story_state(story_id: str) -> StoryState:
    """
    Retrieve the story state for a given story_id.
    """
    if story_id not in story_states:
        raise HTTPException(status_code=404, detail="Story not found")
    return story_states[story_id]

def create_story(story_id: str, genre: str, genre_description: str, location: str, location_description: str, main_character_name: str, main_character_description: str) -> StoryState:
    """
    Create a new story state.
    """
    story_state = StoryState(
        story_id=story_id,
        genre=genre,
        genre_description=genre_description,
        location=location,
        location_description=location_description,
        main_character_name=main_character_name,
        main_character_description=main_character_description,
        paragraphs=[],
        choices=[]
    )
    story_states[story_id] = story_state
    return story_state
