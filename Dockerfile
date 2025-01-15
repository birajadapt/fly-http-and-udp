FROM python:3.12-slim

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry

RUN poetry install --no-root --only main

COPY main.py ./

CMD ["poetry", "run", "python", "main.py"]