FROM python:3.10-bullseye

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

# ENV VARS

EXPOSE 8000

CMD python run.py
