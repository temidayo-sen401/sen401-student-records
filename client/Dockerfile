# Report client service: standard library only, so no pip install is needed.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    API_URL=http://api:8000

WORKDIR /client
COPY report.py .

USER nobody
CMD ["python", "report.py"]
