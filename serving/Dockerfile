FROM python:3-slim-buster
WORKDIR /app
COPY ./app .
COPY models/model1.h5 models/model1.h5
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]