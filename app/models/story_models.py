from pydantic import BaseModel
from typing import List, Optional

class StartStoryInput(BaseModel):
    genre: str
    genre_description: str
    main_character_name: str
    main_character_description: str
    location: str
    location_description: str

class UserChoice(BaseModel):
    story_id: str
    choice: str

class StoryState(BaseModel):
    story_id: str
    genre: str
    genre_description: str
    location: str
    location_description: str
    main_character_name: str
    main_character_description: str
    paragraphs: List[str] = []
    choices: List[str] = []
    current_state: Optional[str] = None
    story_progress: int = 1

# TODO: Implement a more sophisticated story progress tracking system
# that maps integers to story stages (e.g., 1-4: intro, 5-9: rising action, etc.)