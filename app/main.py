from fastapi import FastAPI
from app.api.endpoints import start_story, generate_paragraph

app = FastAPI()

app.include_router(start_story.router, prefix="/start_story", tags=["start_story"])
app.include_router(generate_paragraph.router, prefix="/paragraph", tags=["paragraph"])