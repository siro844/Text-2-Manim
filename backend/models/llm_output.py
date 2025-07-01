from pydantic import BaseModel,Field

class LLMOutput(BaseModel):
    manim_code:str=Field(description="The manim code which needs to be executed to generate the animation")
    file_name:str=Field(description="The name of the file where the manim code should be saved.It should not contain any spaces")
    class_name:str=Field(description="The name of the class that contains the manim code to be executed")
    