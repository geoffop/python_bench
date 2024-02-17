from pyperf._bench import BenchmarkSuite
import glob
import os
import pandas as pd

# Initialize an empty list to store benchmark results
results = []

# Iterate over JSON files in the "results" directory
for file in glob.glob(os.path.join(os.getcwd(), "results", "*.json")):
    # Extract the Python version from the file path
    ver = os.path.splitext(os.path.basename(file))[0]

    # Load the benchmark suite from the JSON file
    benchmark_suite = BenchmarkSuite.load(file)

    # Get benchmark names
    benchmark_names = benchmark_suite.get_benchmark_names()

    # Process each benchmark
    for name in benchmark_names:
        try:
            benchmark = benchmark_suite.get_benchmark(name)
            if benchmark:
                # Extract values from benchmark runs
                for run in benchmark.get_values():
                    results.append({"test": name, "value": run, "python_ver": ver})
        except KeyError:
            # Ignore bonus benchmarks
            pass

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Write results to HTML and JSON files
df.to_html("results.html", index=False)
df.to_json("results.json", orient="records")
