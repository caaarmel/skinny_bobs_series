import argparse #arguments
import subprocess #lets python run other progrems (ie: refine.bat)
import os #file paths and folders
import sys #can exit the program on error

REFINE_CLI = r"C:\Users\Carmel Luttrell\OneDrive\Documents\openrefine-3.7.9\refine.bat"
TRANSFORM_JSON = r"dev\transform\OPENREFINE - Template - Skinny_Series.json"

def run_openrefine_pipeline(input_path, output_path):
    base_filename = os.path.splitext(os.path.basename(input_path))[0]
    project_name = "Auto_" + base_filename

    if not output_path:
        output_dir = os.path.join("dev","import","cleaned")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{base_filename}_transformed.csv")

    print(f"\nCreating project: {project_name}")

    '''
        # 1. run openrefine and create openrefine project
        subprocess.run([
            REFINE_CLI, "create-project",
            f"--file", input_path,
            f"--name", project_name
        ], check=True)

        print("applying transformation...")
    '''
    result = subprocess.run([
        REFINE_CLI, "create-project",
        "--file", input_path,
        "--name", project_name
        ], check=True, capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)


    # 2. apply transformation
    subprocess.run([
        REFINE_CLI, "apply-operations',"
        f"--project-name", project_name,
        f"--operations", TRANSFORM_JSON
    ], check=True)

    print("exporting cleaned data...")

    os.makedirs(os.path.dirname(output_path), exist_ok=True) #checks folder exists

    # 3. export cleaned data to CSV
    subprocess.run([
        REFINE_CLI, "export-rows",
        f"--project-name", project_name,
        f"--format", "csv",
        f"--output", output_path
    ], check=True)

    print("cleaning up (deleting project)...")

    # 4 delete project
    subprocess.run([
        #REFINE_CLI, "delete-project",
        REFINE_CLI, "keep",
        f"--project-name", project_name
    ], check=True)

    print("done, output saved to: {os.path.abspath(output_path)}")

    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Run OpenRefine transformation via CLI.')
        parser.add_argument('--input', required=True, help="path to new input txt file")
        parser.add_argument('--output', required=True, help="path to save the output csv file")
        args = parser.parse_args()

        if not os.path.isfile(args.input):
            print(f"input file not found: {args.input}")
            sys.exit(1)

        run_openrefine_pipeline(args.input, args.output)

