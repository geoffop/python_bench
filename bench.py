import sys
import subprocess
import argparse

# Create an argument parser
parser = argparse.ArgumentParser(description='Run pyperformance with specified OS type and Python version.')
parser.add_argument('--os_type', type=str, required=True, help='The OS type.')
parser.add_argument('--python_ver', type=str, required=True, help='The Python version.')

# Parse the arguments
args = parser.parse_args()

# Run pyperformance with specified benchmarks and output to a JSON file
subprocess.run(["pyperformance", "run", "-f", "-o", f"{args.os_type}_{args.python_ver}.json", "-b", "2to3,chameleon,docutils,html5lib,tornado_http"], check=True)
