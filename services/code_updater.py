import os
import git
from services.vulnerability_generator import generate_vulnerability

def apply_vulnerability():
    file_path, vulnerable_code = generate_vulnerability()
    
    # Ensure the file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return
    
    # Read the current content of the file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Append the vulnerable code to the end of the file
    with open(file_path, 'a') as file:
        file.write("\n\n# New vulnerable code\n")
        file.write(vulnerable_code)
    
    # Commit the changes
    repo = git.Repo('.')
    repo.git.add(file_path)
    repo.index.commit(f"Added new vulnerability to {file_path}")
    
    print(f"Vulnerability added to {file_path}")

if __name__ == '__main__':
    apply_vulnerability()
