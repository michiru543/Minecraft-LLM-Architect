# chains/model6_structure_json.py
import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.load_functions import load_text_file, load_json_file

load_dotenv()
model_name = os.getenv("MODEL_NAME")
structure_example_path = "examples/structure_example.json"
structure_example = load_json_file(structure_example_path)
prompt_path = "prompts/structure_json.txt"
prompt_text = load_text_file(prompt_path)
prompt = ChatPromptTemplate.from_template(prompt_text)

llm_strict = ChatGoogleGenerativeAI(model=model_name, temperature=0.0)
chain = prompt | llm_strict

def generate_structure_json(style, modules, layout, connections, furniture, material_list):
    inputs = {
        "style_description": style,
        "module_names": modules,
        "layout": layout,
        "connections": connections,
        "furniture": furniture,
        "structure_example": structure_example,
        "material_names": material_list
    }
    response = chain.invoke(inputs)
    content = response.content if hasattr(response, "content") else str(response)
    usage = {}
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        usage = response.usage_metadata
    elif hasattr(response, "response_metadata"):
        usage = response.response_metadata.get("usage_metadata", {})
    return content, usage