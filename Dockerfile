FROM python:3.9

WORKDIR /opt/app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]ls