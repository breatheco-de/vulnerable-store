import os
import git
from services.vulnerability_generator import generate_vulnerability
from models import db, Vulnerability
from datetime import datetime
import logging

def apply_vulnerability():
    logging.debug("Starting apply_vulnerability function")
    try:
        file_path, vulnerable_code, vulnerability_type, exploit_info, fix_info = generate_vulnerability()
        
        # Ensure the file exists
        if not os.path.exists(file_path):
            logging.error(f"Error: File {file_path} does not exist.")
            raise FileNotFoundError(f"File {file_path} does not exist.")
        
        # Read the current content of the file
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Append the vulnerable code to the end of the file
        with open(file_path, 'a') as file:
            file.write("\n\n# New vulnerable code\n")
            file.write(vulnerable_code)
        
        logging.debug(f"Vulnerable code appended to {file_path}")
        
        # Commit the changes
        try:
            repo = git.Repo('.')
            repo.git.add(file_path)
            commit = repo.index.commit(f"Added new vulnerability to {file_path}")
            logging.debug(f"Changes committed: {commit.hexsha}")
        except Exception as e:
            logging.error(f"Error committing changes: {str(e)}")
            raise
        
        # Store vulnerability information in the database
        try:
            vulnerability = Vulnerability(
                type=vulnerability_type,
                file_path=file_path,
                date_added=datetime.utcnow(),
                description=f"Commit: {commit.hexsha[:7]}",
                exploit_info=exploit_info,
                fix_info=fix_info
            )
            db.session.add(vulnerability)
            db.session.commit()
            logging.debug("Vulnerability information stored in the database")
        except Exception as e:
            logging.error(f"Error storing vulnerability in database: {str(e)}")
            db.session.rollback()
            raise
        
        logging.debug("apply_vulnerability function completed successfully")
    except Exception as e:
        logging.error(f"Error in apply_vulnerability function: {str(e)}")
        db.session.rollback()
        raise

if __name__ == '__main__':
    apply_vulnerability()
