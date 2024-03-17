FROM python:latest
WORKDIR /usr/agent
ENV PYTHONPATH=/usr/agent
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "src/main.py"]