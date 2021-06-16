import yaml
from pathlib import Path

with open(str(Path.home()) + "/.Pfdata.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

for section in cfg:
    print(section)

