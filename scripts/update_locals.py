import json
import argparse
import hcl2

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--org-dir", required=True, help="Organization directory")
args = parser.parse_args()

# Load payload
with open("payload.json", "r") as f:
    payload = json.load(f)

# Load existing locals.tf
with open(f"{args.org_dir}/locals.tf", "r") as f:
    locals_data = hcl2.load(f)

# Add new repository to locals
new_repo = {
    payload["repository_name"]: {
        "description": payload["description"],
        "language": payload["language"],
        "visibility": payload["visibility"],
        "features": {
            "issues": payload["enable_issues"],
            "wiki": payload["enable_wiki"],
        },
    }
}
locals_data["locals"][0]["repositories"].update(new_repo)

# Write updated locals.tf
with open(f"{args.org_dir}/locals.tf", "w") as f:
    f.write(hcl2.dumps(locals_data))
