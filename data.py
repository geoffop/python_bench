from pathlib import Path
from pyperf._bench import BenchmarkSuite
import glob, os
import pandas as pd

results = []
for file in glob.glob(os.getcwd() + "/results/*.json"):
    ver = file.replace(".json", "").split("/")[-1]
    benchmark_names = []
    first = True
    benchmark_suite = BenchmarkSuite.load(file)

    if first:
        benchmark_names = benchmark_suite.get_benchmark_names()
        first = False
    bench_name = Path(benchmark_suite.filename).name

    for name in benchmark_names:
        try:
            benchmark = benchmark_suite.get_benchmark(name)
            if benchmark is not None:
                for run in benchmark.get_values():
                    results.append({"test": name, "value": run, "python_ver": ver})
        except KeyError:
            # Bonus benchmark! ignore.
            pass

df = pd.DataFrame(results)
data = df.T.to_dict().values()
with open("results.html", "w") as f:
    f.write(df.to_html())
with open("results.json", "w") as f:
    f.write(df.to_json(orient="records"))
