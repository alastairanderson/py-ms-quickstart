import zipfile
from utilities.core.OsUtils import OsUtils

class ZipFileUtils:
    
    @staticmethod
    def extract_to_directory(zip_file_path, extraction_directory):
        if OsUtils.does_file_exist(zip_file_path):
            # Create directory to extract to
            OsUtils.create_directory(extraction_directory)
            
            # Extract file
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(extraction_directory)
            zip_ref.close()