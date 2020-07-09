ARG BASE_IMAGE_TAG
FROM python:${BASE_IMAGE_TAG}

ENV USER=gunicorn
ENV UID=1000
ENV GID=1000
ENV APP_DIR=/app

RUN addgroup \
    --gid $GID \
    $USER \
&& adduser \
    --disabled-password \
    --gecos "" \
    --home $APP_DIR \
    --ingroup $USER \
    --uid $UID \
    $USER

USER $UID

ENV PATH="${APP_DIR}/.local/bin:${PATH}"

WORKDIR $APP_DIR

ARG GUNICORN_VERSION
ARG GUNICORN_STOP_VERSION
RUN pip install --no-cache-dir gunicorn>=${GUNICORN_VERSION}<${GUNICORN_STOP_VERSION}

EXPOSE 8080

ENTRYPOINT ["gunicorn"]
CMD ["-b 0.0.0.0:8080", "-w 3", "main:app"]
