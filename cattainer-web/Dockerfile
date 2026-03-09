#Have the base image be a lightweight modern debian version
FROM python:3.11-slim-bookworm

#Create the folder for this application
WORKDIR /usr/local/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Setup an app user so the container doesn't run as the root user
RUN useradd app

#Copy source files into this new working directory
COPY --chown=app:app . .

#Give the app user ownership of the working directory itself
RUN chown -R app:app /usr/local/app

USER app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
