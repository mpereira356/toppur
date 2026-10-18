FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HOST=0.0.0.0 PORT=3030
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --uid 10001 toppur
COPY app.py run.py catalog.py photo_sources.json ./
COPY templates/ ./templates/
COPY static/ ./static/
RUN mkdir -p /app/instance && chown toppur:toppur /app/instance
USER toppur
EXPOSE 3030
CMD ["python", "run.py"]
