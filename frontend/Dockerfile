FROM python:3.11 as build-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim
RUN apt-get update -y && apt-get install build-essential -y

WORKDIR /app
COPY --from=build-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pwd 
COPY  . .

EXPOSE 8000
CMD ["streamlit", "run", "home.py", "--server.port", "8000"]