from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import time
import re

model = LlamaCpp(
    model_path="vikhr-llama3.1-8b-instruct-r-21-09-24-q4_k_m.gguf",
    n_gpu_layers=32,
    n_batch=512,
    n_ctx=2048,
    f16_kv=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler]),
    verbose=False,
    max_tokens=256,
    temperature=0.5,
)

app = FastAPI()

@app.middleware("http")
async def log_execution_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    execution_time = time.time() - start_time
    print(f"Запрос {request.url.path} выполнен за {execution_time:.4f} секунд.")
    return response

class Query(BaseModel):
    person_data: str


PROMPT = PromptTemplate(
    input_variables=["person_data"],
    template="""<<SYS>>Ты копирайтер, которы пишет людям поздравления с праздниками \
        Сгенерируй поздравление с учетом выданных тебе данных. \
        Не добавляй подпись отправителя, это должен быть только текст поздравления \
        Начало и конец поздравления отделяй токеном <PAD>.<</SYS>> Данные: {person_data} \
        Поздравление: """,
)

chain_generator = PROMPT | model 

@app.post("/generate/")
def generate_message(query: Query):
    result_generator = chain_generator.invoke({"person_data" : query.person_data})
    match = re.search(r"<PAD>(.*?)<?PAD>", result_generator)
    text = match.group(1).strip("<>. ")

    return {"out": text}
