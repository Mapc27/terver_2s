FROM python:3.8.3

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.1.8 && poetry config virtualenvs.create false

WORKDIR .
COPY pyproject.toml .
RUN poetry install --no-dev

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]