ARG tag
FROM python:${tag}
RUN mkdir test
WORKDIR /test
RUN python3 -m pip install pyperformance
RUN pyperformance run -f -o result.json -b apps,serialize
