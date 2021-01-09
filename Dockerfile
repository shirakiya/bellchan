FROM python:3.7.1

ENV TZ Asia/Tokyo

WORKDIR /opt/bellchan

COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN pip install -U pip \
    && pip install -U pipenv \
    && pipenv install --system

COPY ./run.py .
COPY ./bellchan bellchan

CMD ["python", "run.py"]
