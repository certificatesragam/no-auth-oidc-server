FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV=production
COPY server.py ./
EXPOSE 5000
CMD ["python", "server.py"]
