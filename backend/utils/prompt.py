from langchain_core.prompts import PromptTemplate
from backend.utils.parser import parser
prompt = PromptTemplate(
    template="""
    You are tasked with generating manim code to animate the user's request.
    Guidelines to follow:
    1 The code should produce a high quality animation that is visuallay appealing.
    2 If there is any text in the animation it should be clear and readable.
    3 Text in the animation should not overlap any other text in the animation making it harder to read.
    4 The code should explain user's topic in a clear manner.
    5 Always keep the animation as centre as possible and not too far right or left.
    6 Make sure the text present is short and concise.
    7 The animation should be entirely visible and not cut off at the edges.
    
    Also Remember the code you output should be valid and will be executed in a isolated environment to generate the animation video.
    .
    \n{format_instructions}\n
    {topic}\n""",
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)