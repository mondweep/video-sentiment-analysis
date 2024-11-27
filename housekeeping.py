import os
import time
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def cleanup_old_captures(captures_dir='static/captures', minutes=5):
    """
    Delete .jpg files older than specified minutes from the captures directory
    """
    try:
        # Get current time
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(minutes=minutes)
        
        # Ensure the directory exists
        if not os.path.exists(captures_dir):
            logging.warning(f"Directory {captures_dir} does not exist!")
            return
        
        # Counter for deleted files
        deleted_count = 0
        kept_count = 0
        
        # Iterate through files in directory
        for filename in os.listdir(captures_dir):
            if filename.endswith('.jpg'):
                file_path = os.path.join(captures_dir, filename)
                
                # Get file's last modification time
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                # If file is older than cutoff time, delete it
                if file_time < cutoff_time:
                    os.remove(file_path)
                    deleted_count += 1
                    logging.info(f"Deleted: {filename} (Created at: {file_time})")
                else:
                    kept_count += 1
                    logging.debug(f"Kept: {filename} (Created at: {file_time})")
        
        logging.info(f"Cleanup completed. Deleted {deleted_count} files, kept {kept_count} files.")
        logging.info(f"Cutoff time was: {cutoff_time}")
        
    except Exception as e:
        logging.error(f"An error occurred during cleanup: {str(e)}")

if __name__ == "__main__":
    cleanup_old_captures(minutes=5) 