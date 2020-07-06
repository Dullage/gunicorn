ARG BASE_IMAGE_TAG
FROM python:${BASE_IMAGE_TAG}

ARG GUNICORN_VERSION
RUN pip install --no-cache-dir gunicorn==${GUNICORN_VERSION}

EXPOSE 80

WORKDIR /app

ENV USER=gunicorn
ENV UID=1000
ENV GID=1000

RUN addgroup \
    --gid $GID \
	"$USER"

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --ingroup "$USER" \
    --no-create-home \
    --uid $UID \
    "$USER"

USER $UID

ENV GUNICORN_MODULE_NAME="main"
ENV GUNICORN_VARIABLE_NAME="app"
ENV GUNICORN_CMD_ARGS="-w 3 -b 0.0.0.0:8000"

CMD ["gunicorn", "$GUNICORN_MODULE_NAME:$GUNICORN_VARIABLE_NAME"]
