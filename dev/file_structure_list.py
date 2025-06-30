import os

def print_tree(base_path, skip_dirs={'.venv'}, output_file="project_structure.txt"):
    with open(output_file, "w") as f:
        for root, dirs, files in os.walk(base_path):
            # Skip any paths containing a directory to skip
            parts = root.split(os.sep)
            if any(skip in parts for skip in skip_dirs):
                continue
            level = root.replace(base_path, "").count(os.sep)
            indent = "  " * level
            f.write(f"{indent}{os.path.basename(root)}/\n")

            # Still show the folder even if it's empty
            if not files:
                continue

            sub_indent = "  " * (level + 1)
            for file in files:
                f.write(f"{sub_indent}{file}\n")

print_tree(base_path="..")  # Adjust as needed for your working directory

'''
base_path	Meaning
"."	Start from the current folder the script is run from
".."	Start from one folder above the current script
"./dev"	Only show what's inside the dev/ folder
"C:/Users/YourName/Documents"	Use a full path to start from anywhere

'''