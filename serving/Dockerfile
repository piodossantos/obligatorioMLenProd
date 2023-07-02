FROM ubuntu:20.04

# Actualizar los repositorios
RUN sed -i 's/hirsute/focal/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get upgrade -y

# Instalar Python y pip
RUN apt-get install -y python3 python3-pip

WORKDIR /app
COPY ./app .
COPY models/model1.h5 models/model1.h5
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]