FROM python:alpine
LABEL maintainer.name="Tymur Lysenko"\
      maintainer.email="tymur.lysenko@gmail.com"

# Install build dependencies
RUN apk --no-cache\
    add\
    build-base\
    libffi-dev\
    libxml2-dev\
    libxslt-dev\
    openssl-dev\
    postgresql-dev

# Copy file with dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt
