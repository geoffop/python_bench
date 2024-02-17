import os
import sys

# Get the environment name from the TOX_ENV_NAME environment variable
os_ver = '.'.join(map(str, sys.version_info[:3]))

# Run pyperformance with specified benchmarks and output to a JSON file
os.system(f"pyperformance run -f -o {os_ver}.json -b 2to3,chameleon,docutils,html5lib,tornado_http")

# Create a 'results' directory if it doesn't exist
newpath = 'results'
if not os.path.exists(newpath):
    os.makedirs(newpath)

# Move the generated JSON file to the 'results' directory
os.rename(f"{os_ver}.json", f"{newpath}/{os_ver}.json")
