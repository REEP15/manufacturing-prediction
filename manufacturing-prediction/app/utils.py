from werkzeug.utils import secure_filename
import os

def save_file(file, upload_directory: str):
    # Secure the file name
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_directory, filename)
    
    # Save the file
    file.save(file_path)
    return file_path
