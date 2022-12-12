import os
os_ver = os.environ['TOX_ENV_NAME']
os.system(f"pyperformance run -f -o {os_ver}.json -b 2to3,chameleon,docutils,html5lib,tornado_http")
newpath = 'results' 
if not os.path.exists(newpath):
    os.makedirs(newpath)
os.rename(f"{os_ver}.json", f"results/{os_ver}.json")
