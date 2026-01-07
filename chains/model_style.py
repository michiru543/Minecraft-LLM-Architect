# chains/model1_style.py
import os
import base64
import mimetypes
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from utils.load_functions import load_text_file

load_dotenv()
model_name = os.getenv("MODEL_NAME")
prompt_path = "prompts/style.txt"
prompt_text = load_text_file(prompt_path)
prompt = ChatPromptTemplate.from_template(prompt_text)

llm_creative = ChatGoogleGenerativeAI(model=model_name, temperature=0.9)

def get_style_description(user_input_text: str, material_list: str, image_path: str = None):
    inputs = {
        "user_input": user_input_text,
        "material_names": material_list
    }
    text_prompt = prompt.format(**inputs)

    if not image_path:
        response = llm_creative.invoke(text_prompt)
    else:
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            mime_type = "image/jpeg"

        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        message = HumanMessage(content=[
            {"type": "text", "text": text_prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_data}"
                }
            }
        ])

        response = llm_creative.invoke([message])

    content = response.content if hasattr(response, "content") else str(response)

    usage = {}
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        usage = response.usage_metadata
    elif hasattr(response, "response_metadata"):
        usage = response.response_metadata.get("usage_metadata", {})
    return content, usage