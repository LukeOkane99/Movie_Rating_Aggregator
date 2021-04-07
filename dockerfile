FROM alpine:latest

RUN apk add --no-cache python3-dev
RUN apk add py3-pip \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN apk add --update musl-dev gcc libffi-dev libxml2-dev libxslt-dev build-base
RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["run_app.py"]