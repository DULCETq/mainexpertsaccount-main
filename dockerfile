# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /MainExpertsAuthService
COPY requirements.txt /MainExpertsAuthService/
RUN pip install -r requirements.txt
COPY . /MainExpertsAuthService/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh