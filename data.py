import pandas as pd
import subprocess
import os
clean_dict = {}
for root, _, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith((".json")):
            f = subprocess.run(f"pyperformance show {file}",shell=True, check=True, capture_output=True, text=True).stdout
            data = f.split('\n')
            for datapoint in data:
                if datapoint.__contains__("#"):
                    first = datapoint
                    break
            else:
                first = None
            index = data.index(first)
            clean_data = []
            for x in data[index::]:
                if x != "":
                    clean_data.append(x)
            keys = clean_data[::2]
            vals = clean_data[1::2]
            vals = [val.replace('Mean +- std dev: ', '') for val in vals]
            clean_dict[file.replace(".json","")] = dict(zip(keys, vals))
df = pd.DataFrame.from_dict(clean_dict, orient="index")
print(df)
