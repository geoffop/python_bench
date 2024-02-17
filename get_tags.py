import requests
import json

# Determine the Docker Hub URL based on whether the system uses '/' in the Python image name
if '/' in 'python':
    hub = "https://registry.hub.docker.com/v2/repositories/python/tags/"
else:
    hub = "https://registry.hub.docker.com/v2/repositories/library/python/tags/"

# Get the total number of pages
response = requests.get(hub)
data = json.loads(response.text)
count = data.get("count", 0)
pagination = len(data.get("results", []))
pages = count // pagination + 1

# Retrieve all tags page by page
tags = []
for i in range(1, pages + 1):
    response = requests.get(f"{hub}?page={i}")
    page_data = json.loads(response.text)
    ptags = [entry["name"] for entry in page_data.get("results", [])]
    tags.extend(ptags)

# Write the tags to a file
with open("tags.txt", "w") as f:
    f.write("\n".join(tags))
