import os
import sys
import pyperf

# Get the Python version
os_ver = '.'.join(map(str, sys.version_info[:3]))

# Create a runner object
runner = pyperf.Runner()

# Add benchmarks
benchmarks = ['2to3', 'chameleon', 'docutils', 'html5lib', 'tornado_http']
for bench in benchmarks:
    runner.bench_time_func(bench, lambda: os.system(f"pyperformance run -f -b {bench}"))

# Save results to a JSON file
runner.save(f"{os_ver}.json")

# Create a 'results' directory if it doesn't exist
newpath = 'results'
if not os.path.exists(newpath):
    os.makedirs(newpath)

# Move the generated JSON file to the 'results' directory
os.rename(f"{os_ver}.json", f"{newpath}/{os_ver}.json")
