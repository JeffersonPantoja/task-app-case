FROM python:3.9.18-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY todo_project ./todo_project

WORKDIR /app/todo_project

EXPOSE 5000

CMD ["python", "-c", "from todo_project import app; app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)"]
