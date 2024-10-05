from typing import Dict, Tuple

STORY_STAGES: Dict[int, Tuple[str, str]] = {
    1: ("Exposition", "Introduce the world, characters, and initial situation. Set the scene and provide background."),
    2: ("Inciting Incident", "Present an event that disrupts the status quo and sets the main plot in motion."),
    3: ("Rising Action", "Build tension with a series of events. Protagonist faces increasing challenges."),
    4: ("First Plot Point", "Introduce a significant event that fully commits the protagonist to their journey."),
    5: ("Midpoint", "Present a turning point that raises the stakes or shifts perspective."),
    6: ("Rising Complications", "Intensify obstacles and antagonist's presence. Test relationships and internal conflicts."),
    7: ("Second Plot Point", "Introduce the final piece of information needed to propel the story towards its climax."),
    8: ("Climax", "Present the peak of tension and conflict. Main conflict comes to a head."),
    9: ("Falling Action", "Show immediate aftermath of the climax. Begin tying up loose ends."),
    10: ("Resolution", "Resolve remaining plot points and establish a new equilibrium.")
}

def get_story_stage(story_progress: int) -> Tuple[str, str]:
    """
    Get the current story stage based on the story progress.
    
    :param story_progress: An integer from 1 to 10 representing the current story progress.
    :return: A tuple containing the stage name and description.
    """
    if story_progress < 1 or story_progress > 10:
        raise ValueError("Story progress must be between 1 and 10.")
    
    return STORY_STAGES[story_progress]

def get_story_context(story_progress: int) -> str:
    """
    Get the story context based on the current story progress and the next stage.
    
    :param story_progress: An integer from 1 to 10 representing the current story progress.
    :return: A string describing the expected story context for current and next stages.
    """
    current_stage_name, current_stage_description = get_story_stage(story_progress)
    current_context = f"The reader is currently at stage {story_progress}/10 ({current_stage_name}). {current_stage_description}"
    
    if story_progress < 10:
        next_stage_name, next_stage_description = get_story_stage(story_progress + 1)
        next_context = f"The next stage will be {story_progress + 1}/10 ({next_stage_name}). {next_stage_description}"
    else:
        next_context = "This is the final stage of the story."
    
    return f"{current_context}\n\nLooking ahead: {next_context}"