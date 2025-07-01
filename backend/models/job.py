from enum import Enum
from pydantic import BaseModel, Field


class JobRequest(BaseModel):
    topic: str = Field(
        description="The Topic for which the animation needs to be generated"
    )


class JobResponse(BaseModel):
    job_id: str = Field(description="Unique identifier for the job")
    status: str = Field(
        description="Status of the job, e.g., 'pending', 'running', 'completed', 'failed'"
    )
    video_url: str | None = Field(
        default=None, description="URL of the generated video if available"
    )
    logs: str | None = Field(
        default=None, description="Logs from the rendering process if available"
    )
