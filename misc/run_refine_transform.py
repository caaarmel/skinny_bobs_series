import argparse
import os
import sys
import requests
import json
import subprocess
import time

REFINE_HOST = "http://127.0.0.1:3333"
TRANSFORM_JSON = os.path.join(os.path.dirname(__file__), "openrefine_template_skinny_series.json")
REFINE_BAT_PATH = r"C:\\Users\\Carmel Luttrell\\OneDrive\\Documents\\openrefine-3.7.9\\refine.bat"

def ensure_openrefine_running():
    try:
        response = requests.get(f"{REFINE_HOST}/command/core/get-version")
        if response.status_code == 200:
            print("🟢 OpenRefine is already running.")
            return
    except requests.exceptions.ConnectionError:
        print("🟡 OpenRefine not detected — starting it...")

    subprocess.Popen(['cmd.exe', '/c', REFINE_BAT_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)

    try:
        response = requests.get(f"{REFINE_HOST}/command/core/get-version")
        if response.status_code == 200:
            print("✅ OpenRefine started successfully.")
        else:
            print("❌ Failed to verify OpenRefine after launch.")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to OpenRefine after launching.")
        sys.exit(1)

def create_project(file_path, project_name):
    print("\n📁 Creating project...")

    print("\n📘 Listing all projects BEFORE creation")
    pre_projects = requests.get(f"{REFINE_HOST}/command/core/get-all-project-metadata").json()
    for pid, proj in pre_projects.get("projects", {}).items():
        print(f"  - {pid}: {proj.get('name')}")

    # ✅ Get CSRF token first
    csrf_resp = requests.get(f"{REFINE_HOST}/command/core/get-csrf-token")
    if csrf_resp.status_code != 200:
        print("❌ Failed to get CSRF token")
        print(csrf_resp.text)
        sys.exit(1)

    csrf_token = csrf_resp.text.strip('"')  # Remove double quotes from token

    with open(file_path, 'rb') as file_data:
        response = requests.post(
            f"{REFINE_HOST}/command/core/create-project-from-upload",
            headers={"X-CSRF-Token": csrf_token},
            files={'project-file': file_data},
            data={
                'project-name': project_name,
                'format': 'text/line-based',
                'separator': '\t',
                'header-lines': '1',
                'storeBlankRows': 'true'
            }
        )

    print(f"🔍 Raw response from create-project:\n{response.status_code}\n{response.text}")

    if response.status_code != 200 or "error" in response.text.lower():
        print("❌ Failed to create project")
        sys.exit(1)

    print("✅ Project created")

    print("\n📘 Listing all projects AFTER creation")
    all_projects = requests.get(f"{REFINE_HOST}/command/core/get-all-project-metadata").json()
    for pid, proj in all_projects.get("projects", {}).items():
        print(f"  - {pid}: {proj.get('name')}")

    project_name_lower = project_name.lower()
    for pid, data in all_projects.get("projects", {}).items():
        actual_name = data.get("name") or data.get("meta", {}).get("name")
        print(f"🔎 Found project: {actual_name} (ID: {pid})")
        if actual_name and project_name_lower in actual_name.lower():
            return pid

    print(f"❌ Project name '{project_name}' not found in:")
    for pid, data in all_projects.get("projects", {}).items():
        print(f"  • {pid}: {data.get('name') or data.get('meta', {}).get('name')}")
    sys.exit(1)


def apply_operations(project_id):
    print("\n⚙️ Applying transformation...")
    with open(TRANSFORM_JSON, 'r') as ops_file:
        operations = ops_file.read()

    response = requests.post(
        f"{REFINE_HOST}/command/core/apply-operations?project={project_id}",
        headers={"Content-Type": "application/json"},
        data=operations
    )
    if response.status_code != 200:
        print("❌ Failed to apply transformation")
        print(response.text)
        sys.exit(1)
    print("✅ Transformation applied")

def export_rows(project_id, output_path):
    print("\n📤 Exporting cleaned data...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    params = {
        "project": project_id,
        "engine": json.dumps({"facets": [], "mode": "row-based"}),
        "format": "csv"
    }

    export_resp = requests.get(
        f"{REFINE_HOST}/command/core/export-rows",
        params=params
    )

    if export_resp.status_code != 200:
        print("❌ Failed to export data")
        print(export_resp.text)
        sys.exit(1)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(export_resp.text)

    full_path = os.path.abspath(output_path)
    print(f"✅ Exported to {full_path}")

def delete_project(project_id):
    print("\n🧹 Deleting project...")
    response = requests.post(
        f"{REFINE_HOST}/command/core/delete-project",
        data={"project": project_id}
    )
    if response.status_code != 200:
        print("❌ Failed to delete project")
        print(response.text)
        sys.exit(1)
    print("✅ Project deleted")

def run_openrefine_pipeline(input_path, output_path=None):
    ensure_openrefine_running()

    base_filename = os.path.splitext(os.path.basename(input_path))[0]
    project_name = "Auto_" + base_filename

    if not output_path:
        output_dir = os.path.join("dev", "import", "cleaned")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{base_filename}_transformed.csv")

    project_id = create_project(input_path, project_name)
    print(f"🔍 Using project ID: {project_id}")
    apply_operations(project_id)
    export_rows(project_id, output_path)
    delete_project(project_id)

    print(f"\n✅ Done! Output saved to: {os.path.abspath(output_path)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run OpenRefine transformation via API.')
    parser.add_argument('--input', required=True, help='Path to the input TXT file')
    parser.add_argument('--output', required=False, help='(Optional) Path to save the output CSV file')
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"❌ Input file not found: {args.input}")
        sys.exit(1)

    run_openrefine_pipeline(args.input, args.output)
