import os
import git
from services.vulnerability_generator import generate_vulnerability
from models import db, Vulnerability
from datetime import datetime

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
    commit = repo.index.commit(f"Added new vulnerability to {file_path}")
    
    # Store vulnerability information in the database
    vulnerability = Vulnerability(
        type=file_path.split('/')[-1].split('.')[0],  # Use the file name as the vulnerability type
        file_path=file_path,
        date_added=datetime.utcnow(),
        description=f"Commit: {commit.hexsha[:7]}"
    )
    db.session.add(vulnerability)
    db.session.commit()
    
    print(f"Vulnerability added to {file_path} and stored in the database")

if __name__ == '__main__':
    apply_vulnerability()
