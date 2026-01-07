# chains/model7_code.py
import os
import re
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.load_functions import load_text_file

load_dotenv()
model_name = os.getenv("MODEL_NAME")
code_example = load_text_file("examples/code_example.py")
prompt_path = "prompts/code.txt"
prompt_text = load_text_file(prompt_path)
prompt = ChatPromptTemplate.from_template(prompt_text)

llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.1)
chain = prompt | llm

def extract_code_block(response: str) -> str:
    match = re.search(r"```(?:python)?\n(.*?)```", response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return response.strip()

def save_code_to_file(code: str, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not code.strip():
        raise ValueError("code is empty，unsaved.")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

def generate_code_and_save(layout: str, structure_json: str, save_path: str):
    inputs = {
        "layout": layout,
        "structure_json": structure_json,
        "code_example": code_example
    }
    response = chain.invoke(inputs)
    content = response.content if hasattr(response, "content") else str(response)
    code = extract_code_block(content)
    save_code_to_file(code, save_path)

    usage = {}
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        usage = response.usage_metadata
    elif hasattr(response, "response_metadata"):
        usage = response.response_metadata.get("usage_metadata", {})
    return content, usage