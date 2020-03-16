FROM python:3.8

RUN pip install --no-cache-dir gunicorn

EXPOSE 80

CMD gunicorn main:app --chdir /app -w ${WORKERS:-3} -b ${HOST:-'0.0.0.0'}:${PORT:-80}
