# syntax=docker/dockerfile:1

FROM python:3.10.8

RUN pip3 install --upgrade pip
RUN pip install virtualenv 
ENV VIRTUAL_ENV=/venv

RUN virtualenv venv -p python3

ENV PATH="VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# expose port
EXPOSE 5000

# run application
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]