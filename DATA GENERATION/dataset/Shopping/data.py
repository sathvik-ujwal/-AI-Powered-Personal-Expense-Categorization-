import os, json

base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "ambiguous.json"), "r") as f:
    ambiguous = json.load(f)

with open(os.path.join(base_dir, "specific.json"), "r") as f:
    specific = json.load(f)

data = {
    "ambiguous": ambiguous,
    "specific": specific
}
