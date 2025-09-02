FROM python:3.11-slim

# Avoid Python buffering and create a non-root user (optional)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
