FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6

ENV PYTHONPATH=/app
EXPOSE 80
EXPOSE 8888

COPY ./app/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

ARG env=prod

COPY ./app/requirements.dev.txt /tmp
RUN bash -c "if [ $env == 'dev' ] ; then pip install -r /tmp/requirements.dev.txt ; fi" && \
    rm /tmp/requirements.dev.txt

COPY ./app /app
WORKDIR /app/
