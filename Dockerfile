FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

RUN pip3 install poetry

ADD pyproject.toml poetry.lock .env /code/
RUN poetry config virtualenvs.create false && poetry install

COPY . /code/

ENTRYPOINT ["/code/entrypoint"]
CMD ["start-reload"]