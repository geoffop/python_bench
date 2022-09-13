import os

command = "bash get_tags.sh python"
tag_file = "tags.txt"
os.system(command)
with open(tag_file) as f:
    tag_list = f.read().split()
os.remove(tag_file)
print(tag_list)
tag_list = filter(
    lambda x: x[-1].isdigit(), tag_list
)  # not a version based on a distro
tag_list = filter(lambda x: x[0] == "3", tag_list)  # python 3
tag_list = filter(
    lambda x: not any(y.isalpha() for y in x), tag_list
)  # filter out things that have letters
tag_list = filter(
    lambda x: len(x.split(".")) == 3, tag_list
)  # want just versions with a patch version
tag_list = filter(
    lambda x: int(x.split(".")[1]) > 6, tag_list
)  # 3.6 and below doesnt work with benchmark
for version in tag_list:
    os.system("podman system prune -a -f")
    os.system(
        f"podman build -f dockerfile -t clean/test:latest --build-arg tag={version}"
    )
    os.system("podman run --name tester clean/test:latest")
    os.system(f"export container=$(podman ps -alq) && podman cp $container:/test/{version}.json .")
    os.system(f"mkdir --parents ./results && mv ./{version}.json results/{version}.json")
