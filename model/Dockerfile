FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    git \
    && apt-get clean

RUN pip install llama-cpp-python \
--extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY vikhr-llama3.1-8b-instruct-r-21-09-24-q4_k_m.gguf /app

EXPOSE 8000

COPY model.py /app
COPY model_langchain.py /app

CMD ["uvicorn", "model_langchain:app", "--host", "0.0.0.0", "--port", "8000"]