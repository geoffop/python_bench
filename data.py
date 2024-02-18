import glob
import os
import pandas as pd
from pyperf._bench import BenchmarkSuite

# Initialize an empty list to store benchmark results
benchmark_results = []

# Get the current working directory
cwd = os.getcwd()

# Find all JSON files in the current working directory
json_files = glob.glob(os.path.join(cwd, '*.json'))
print(json_files)
# Iterate over all JSON files in the current directory
for json_file in json_files:
    # Extract the Python version and OS type from the file name
    os_type, python_version = os.path.splitext(os.path.basename(json_file))[0].split('_')

    # Load the benchmark suite from the JSON file
    benchmark_suite = BenchmarkSuite.load(json_file)

    # Get the names of all benchmarks in the suite
    benchmark_names = benchmark_suite.get_benchmark_names()

    # Process each benchmark
    for benchmark_name in benchmark_names:
        try:
            # Get the benchmark by name
            benchmark = benchmark_suite.get_benchmark(benchmark_name)
            if benchmark:
                # Extract values from all runs of the benchmark
                for run in benchmark.get_runs():
                    # Append the benchmark name, value, metadata, warmups, Python version, and OS type to the results list
                    benchmark_results.append({
                        "test": benchmark_name,
                        "value": run.values,
                        "python_ver": python_version,
                        "os_type": os_type
                    })
        except KeyError:
            # Ignore benchmarks that are not found in the suite
            pass

# Convert the results list into a pandas DataFrame
benchmark_dataframe = pd.DataFrame(benchmark_results)
print(benchmark_dataframe)
# Ensure the 'values' column is a list
benchmark_dataframe['value'] = benchmark_dataframe['value'].apply(lambda x: list(x) if isinstance(x, tuple) else x)

# Explode the 'value' column into multiple rows
benchmark_dataframe = benchmark_dataframe.explode('value')

# Cast the 'value' column to float
benchmark_dataframe['value'] = benchmark_dataframe['value'].astype(float)

# Remove any rows with NaN as a value
benchmark_dataframe = benchmark_dataframe.dropna()

# Group by 'os', 'python_ver', and 'test' and get the average
benchmark_dataframe = benchmark_dataframe.groupby(['os_type', 'python_ver', 'test']).mean().reset_index()

# Create a new DataFrame that groups by 'os_type', 'python_ver', and 'test' and gets the minimum 'value' for each group
min_values = benchmark_dataframe.groupby(['os_type', 'python_ver', 'test'])['value'].min().reset_index()

# Create a new column 'quantized_value' that quantizes the 'value' column into 4 bins
benchmark_dataframe['quantized_value'] = pd.cut(benchmark_dataframe['value'], bins=4, labels=False)

print(benchmark_dataframe)
