FROM python:3.12-slim-bookworm

ENV LANG=C.UTF-8

ENV APP_DIR=/usr/src/app

RUN apt-get update -y \
    && apt-get install libpq-dev gcc -y

# Create a directory for application
RUN mkdir -p ${APP_DIR}

RUN useradd --create-home appusr

# Make app as working directory
WORKDIR ${APP_DIR}

# Install requirements
COPY requirements.txt ${APP_DIR}
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN chown -R appusr:appusr ${APP_DIR}
USER appusr

# Copy rest of application files to app folder
COPY . ${APP_DIR}

EXPOSE 8000

# Run the start script
CMD ["sh", "start.sh"]
