import os

command = "bash get_tags.sh python"
tag_file = "tags.txt"
os.system(command)
with open(tag_file) as f:
    tag_list = f.read().split()
os.remove(tag_file)
tag_list = filter(
    lambda x: x[-1].isdigit(), tag_list
)  # not a version based on a distro
tag_list = filter(lambda x: x[0].isdigit(), tag_list)  # is version number
tag_list = filter(lambda x: x[0] == "3", tag_list)  # python 3
tag_list = filter(
    lambda x: not x.__contains__("-"), tag_list
)  # no things like 3-stretch
tag_list = filter(
    lambda x: len(x.split(".")) == 3, tag_list
)  # want just versions with a patch version
tag_list = filter(
    lambda x: int(x.split(".")[1]) > 5, tag_list
)  # 3.5 and below doesnt work with benchmark
for version in tag_list:
    os.system(f"docker build dockerfile -t clean/test:latest --build-arg tag={version}")
    os.system("docker run $(docker images | awk '{print $1}' | awk 'NR==2')")
    os.system(
        "export container=$(docker ps -alq) && docker cp $container:/test/result.json ."
    )
    os.system("docker rm $(docker ps --filter status=exited -q)")
    os.system(f"mkdir --parents ./results && mv ./result.json results/{version}.json")
