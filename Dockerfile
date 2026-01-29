FROM python:3.13.2

WORKDIR  /quotes


COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-root


COPY quotes ./


EXPOSE 8000


CMD ["python", "manage.py",  "runserver", "0.0.0.0:8000"]