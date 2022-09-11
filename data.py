# import pandas as pd
# import subprocess
# import os
# clean_dict = {}
# for root, _, files in os.walk(os.getcwd()):
#     for file in files:
#         if file.endswith((".json")):
#             f = subprocess.run(f"pyperformance show {file}",shell=True, check=True, capture_output=True, text=True).stdout
#             data = f.split('\n')
#             for datapoint in data:
#                 if datapoint.__contains__("#"):
#                     first = datapoint
#                     break
#             else:
#                 first = None
#             index = data.index(first)
#             clean_data = []
#             for x in data[index::]:
#                 if x != "":
#                     clean_data.append(x)
#             keys = clean_data[::2]
#             vals = clean_data[1::2]
#             vals = [val.replace('Mean +- std dev: ', '') for val in vals]
#             clean_dict[file.replace(".json","")] = dict(zip(keys, vals))
# df = pd.DataFrame.from_dict(clean_dict, orient="index")
# print(df)
import argparse
import json
from pathlib import Path
from unittest import result
from pyperf._bench import BenchmarkSuite
import glob, os

import seaborn as sns
import pandas as pd

sns.set(style="whitegrid")

# parser = argparse.ArgumentParser(description='Convert a list of benchmarks into a CSV')
# parser.add_argument('files', metavar='N', type=str, nargs='+',
#                     help='files to compare')
# args = parser.parse_args()
results = []
for file in glob.glob(os.getcwd()+"/results/*.json"):
    ver = file.replace(".json","").split("/")[-1]
    benchmark_names = []
    first = True
    benchmark_suite = BenchmarkSuite.load(file)
    if first:
        # Initialise the dictionary keys to the benchmark names
        benchmark_names = benchmark_suite.get_benchmark_names()
        first = False
    bench_name = Path(benchmark_suite.filename).name
    
    for name in benchmark_names:
        try:
            benchmark = benchmark_suite.get_benchmark(name)
            if benchmark is not None:
                results.append({
                    'test': name,
                    'runtime': bench_name.replace('.json', ''),
                    'stdev': benchmark.stdev(),
                    'mean': benchmark.mean(),
                    'median': benchmark.median(),
                    "python_ver": ver
                })
        except KeyError:
            # Bonus benchmark! ignore.
            pass

df = pd.DataFrame(results)
df.to_excel("test.xlsx")
data = df.T.to_dict().values()
print(df.to_html())
with open("results.html", "w") as f:
    f.write(df.to_html(classes='table table-stripped'))
# file_contents = ""
# with open("website/src/components/showcase.astro",'r') as f:
#     file_contents = f.read().replace("$[replacemeorfailtobuild]",json.dumps(list(data)))
# with open("website/src/components/showcase.astro",'w') as f:
#     f.write(file_contents)


