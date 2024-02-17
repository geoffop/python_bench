import sys
import subprocess

# Get the Python version
os_ver = '.'.join(map(str, sys.version_info[:3]))

# Run pyperformance with specified benchmarks and output to a JSON file
subprocess.run(["pyperformance", "run", "-f", "-o", f"{os_ver}.json", "-b", "2to3,chameleon,docutils,html5lib,tornado_http"], check=True)