from http.client import HTTPResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.database.redis import r

from backend.models.job import JobRequest, JobResponse
from backend.utils.manim_code_gen import generate_manim_code

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI backend!"}


@app.get("/status/{job_id}", response_model=JobResponse)
async def get_job_status(job_id: str):
    job_status = r.get(job_id)
    if not job_status:
        return JSONResponse(status_code=404, content="Job not found")
    
    video_url = r.get(f"{job_id}:url")
    print(f"Video URL for job {job_id}: {video_url}")
    print(type(video_url))
    logs = r.get(f"{job_id}:logs")
    response = JobResponse(
        job_id=job_id,
        status=job_status.decode("utf-8") if job_status else "Not Found",
        video_url=video_url.decode("utf-8") if video_url else None,
        logs=logs.decode("utf-8") if logs else None,
    )
    print(response)
    return JSONResponse(status_code=200, content=response.dict())


@app.post("/generate_manim", response_model=JobResponse)
def generate_manim(request:JobRequest) -> str:
    try:
        
        job_id = generate_manim_code(request.topic)
        return JSONResponse(status_code=200, content=JobResponse(job_id=job_id, status="IN_PROGRESS", video_url=None, logs=None).dict())
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
