from pydantic import BaseModel, HttpUrl

class BlueprintRequest(BaseModel):
    url: HttpUrl

class PromptStep(BaseModel):
    step: int
    title: str
    prompt: str

class BlueprintResponse(BaseModel):
    id: str
    url: str
    techStack: str
    frontendPrompts: list[PromptStep]
    backendPrompts: list[PromptStep]
    createdAt: str