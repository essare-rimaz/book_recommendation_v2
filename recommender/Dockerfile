# syntax=docker/dockerfile:1
FROM python:3.9
WORKDIR /recommender/
#RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt /recommender/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . /recommender/
CMD ["uvicorn", "app:app", "--reload"]