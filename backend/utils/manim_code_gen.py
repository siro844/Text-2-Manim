import threading
import uuid
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from backend.utils.parser import LLMOutput, parser
from backend.utils.prompt import prompt
from backend.worker.sandbox_render import sandbox_render
from backend.database.redis import r

load_dotenv()
model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

def generate_manim_code(topic: str) -> str:
    try:
        chain = prompt | model | parser
        response : LLMOutput = chain.invoke({"topic": topic})
        print("Generated Manim Code:")
        print(response)
        with open(f"{response.file_name}.py", "w") as f:
            f.write(response.manim_code)
        print("Manim code generated and saved to manim_code.py")
        job_id = uuid.uuid4().hex
        r.set(job_id,"IN_PROGRESS")
        response.file_name = f"{response.file_name}.py"
        threading.Thread(
            target=sandbox_render,
            args=(response.manim_code, response.file_name, response.class_name, job_id),
            daemon=True
        ).start()
        return job_id
    except Exception as e:
        raise RuntimeError(f"Error generating Manim code: {e}")
