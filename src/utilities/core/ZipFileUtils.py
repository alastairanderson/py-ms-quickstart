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


#region sandbox
# from OsUtils import OsUtils   # need to change the path as its in the same dir - comment ref at top
# import os

# print(os.getcwd())            # check where we are working from before testing

# zip_file_path_1 = "./test.zip"      # need to create this for testing
# extraction_directory_1 = "./test"
# ZipFileUtils.extract_to_directory(zip_file_path_1, extraction_directory_1)
#endregion
