import os
from langchain.prompts import PromptTemplate
import getpass
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

app = FastAPI()

class PatientRequest(BaseModel):
    gender: str
    age: int
    symptons: list[str]

    
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

template="""
Berikan rekomendasi departemen rumah sakit yang sesuai dengan {symptons} yang diberikan
"""

prompt=PromptTemplate(
    input_variables=["gender","age","symptons"],
    template=template,
)

json_schema = {
    "title": "department",
    "description": "suggest the most relevant specialist department in hospital based on symptoms",
    "type": "object",
    "properties": {
        "recommended_department": {
            "type": "string",
            "description": "Name of the department in hospital based on symptoms, like 'Neurology', 'Cardiology', etc",
        }
    },
    "required": ["recommended_department"],
}
structured_llm = model.with_structured_output(json_schema)

chain = prompt | structured_llm

# result= chain.invoke({"symptons": input()})
# print(result)

@app.post("/rekomendasi-departemen")
async def rekomendasi_departemen(data: PatientRequest):
    result = chain.invoke({
        "gender": data.gender,
        "age": data.age,
        "symptons": data.symptons
    })
    return result
