# chains/model2_modules.py
import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.load_functions import load_text_file

load_dotenv()
model_name = os.getenv("MODEL_NAME")
prompt_path = "prompts/modules.txt"
prompt_text = load_text_file(prompt_path)
prompt = ChatPromptTemplate.from_template(prompt_text)

llm_creative = ChatGoogleGenerativeAI(model=model_name, temperature=0.9)
chain = prompt | llm_creative

def generate_module_names(style_description: str):
    response = chain.invoke({"style_description": style_description})
    content = response.content if hasattr(response, "content") else str(response)
    usage = {}
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        usage = response.usage_metadata
    elif hasattr(response, "response_metadata"):
        usage = response.response_metadata.get("usage_metadata", {})
    return content, usage