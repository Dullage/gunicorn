# gunicorn

A Gunicorn Docker base image with Python.

## Tags

* 20.0-python3.8-alpine3.12, latest
* 20.0-python3.8

## Example Usage

Note: By default, this image expects a module called "main" (e.g. main.py) in the /app directory, this should expose a variable called "app".

### No dependencies

If your app has no dependencies then you can simply run:

```bash
docker run -v /path/to/your/app:/app -p 80:80 dullage/gunicorn:20.0-python3.8-alpine3.12
```

### Dependencies

If you want to install dependencies then you can use this as a base image:


```dockerfile
FROM dullage/gunicorn:20.0-python3.8-alpine3.12

COPY /path/to/your/app /app

RUN pip install --no-cache-dir -r /app/requirements.txt
```

```bash
docker build -t my-app .

docker run -p 80:80 my-app
```

## Environment Variables

There are three environment variables that can be used:

`GUNICORN_MODULE_NAME` Defaults to "main".
`GUNICORN_VARIABLE_NAME` Defaults to "app".
`GUNICORN_CMD_ARGS` This is a standard gunicorn environment variable. This docker image defaults this to "-w 3 -b 0.0.0.0:8000" (bind to all interfaces with 3 workers on port 8000 inside the container).
