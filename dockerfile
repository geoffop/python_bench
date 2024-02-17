# Commented Dockerfile

# Set the base image to Python with the specified tag
FROM python:${tag}

# Declare the 'tag' argument (used later)
ARG tag

# Create a directory named 'test'
RUN mkdir test

# Set the working directory to '/test'
WORKDIR /test

# Upgrade pip and install wheel
RUN python3 -m pip install --upgrade pip wheel

# Install pyperformance
RUN python3 -m pip install pyperformance

# Run pyperformance with specified benchmarks and output to a JSON file
RUN pyperformance run -f -o ${tag}.json -b apps,serialize
