FROM python:3.7.1

ENV TZ Asia/Tokyo

WORKDIR /opt/bellchan

COPY ./Pipfile .
COPY ./Pipfile.lock .
COPY ./run.py .
COPY ./bellchan bellchan

RUN pip install -U pip \
    && pip install pipenv \
    && pipenv install --system

CMD ["python", "run.py"]
