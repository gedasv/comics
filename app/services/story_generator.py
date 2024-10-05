from app.models.story_models import UserChoice, StoryState
from app.utils.langchain_utils import generate_story_content, Choice, get_openai_client
from fastapi import HTTPException

# In-memory storage for story states (replace with database later)
story_states: dict[str, StoryState] = {}

def generate_next_paragraph(user_choice: UserChoice):
    """
    Generate the next paragraphs and choices based on the user's input.
    """
    story_id = user_choice.story_id
    story_state = story_states.get(story_id)

    if not story_state:
        raise HTTPException(status_code=404, detail="Story not found")

    context = "\n\n".join(story_state.paragraphs)
    
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
    story_state.paragraphs.extend(result.paragraphs)
    story_state.choices = [Choice(text=choice.text, meta_description=choice.meta_description) for choice in result.choices]
    story_state.current_state = result.paragraphs[-1]  # Set the last paragraph as the current state
    story_state.story_progress += 1
    
    # TODO: Implement a more sophisticated ending condition
    if story_state.story_progress >= 10:
        story_state.choices = [
            Choice(text="End the story", meta_description="The final scene of the story, showing the conclusion"),
            Choice(text="End the story", meta_description="The final scene of the story, showing the conclusion")
        ]
    
    return result.paragraphs, story_state.choices

def get_story_state(story_id: str) -> StoryState:
    """
    Retrieve the story state for a given story_id.
    """
    if story_id not in story_states:
        raise HTTPException(status_code=404, detail="Story not found")
    return story_states[story_id]

def generate_story_title(genre: str, main_character_name: str, location: str) -> str:
    client = get_openai_client()
    prompt = f"Generate a catchy title for a {genre} comic book story featuring {main_character_name} in {location}. The title should be short and engaging."
    
    messages = [
        {"role": "system", "content": "You are a creative comic book title generator."},
        {"role": "user", "content": prompt}
    ]

    completion = client.chat.completions.create(
        model="gpt-4-0613",
        messages=messages,
        max_tokens=20,
        temperature=0.7
    )

    return completion.choices[0].message.content.strip('"')

def create_story(story_id: str, genre: str, genre_description: str, location: str, location_description: str, main_character_name: str, main_character_description: str) -> StoryState:
    """
    Create a new story state.
    """
    title = generate_story_title(genre, main_character_name, location)
    
    story_state = StoryState(
        story_id=story_id,
        title=title,
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
