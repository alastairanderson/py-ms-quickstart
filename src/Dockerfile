FROM python:3.7.3-slim-stretch

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 5000

CMD [ "python", "./main.py" ]
