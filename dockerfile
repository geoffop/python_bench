ARG tag
FROM python:${tag}
ARG tag
RUN mkdir test
WORKDIR /test
RUN python3 -m pip install --upgrade wheel
RUN python3 -m pip install pyperformance
RUN pyperformance run -f -o ${tag}.json -b apps,serialize
