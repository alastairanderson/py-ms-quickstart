import os
from os import listdir
from os.path import isfile, join
from shutil import copyfile, rmtree
import errno

class OsUtils:

    @staticmethod
    def create_directory(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError as ex:
            print("Handle this somehow")


    @staticmethod
    def create_file(file):
        open(file, 'a').close()


    @staticmethod
    def join_directory_path(directory1, directory2):
        return os.path.join(directory1, directory2)


    @staticmethod
    def write_to_file(file, content):
        OsUtils.write_to_file_in_specified_mode(file, content, "w") 


    @staticmethod
    def write_to_file_in_binary_mode(file, content):
        OsUtils.write_to_file_in_specified_mode(file, content, "wb") 


    @staticmethod
    def write_to_file_in_specified_mode(file, content, mode):
        if not os.path.exists(os.path.dirname(file)):
            try:
                os.makedirs(os.path.dirname(file))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(file, mode) as f:
            f.write(content)
            f.close()       


    @staticmethod
    def read_from_file(file_path):
        try:
            file = open(file_path, "r")
            contents = file.read()
            file.close()
            return contents
        except Exception:
            print("Could not read file " + file_path)


    @staticmethod
    def read_lines_from_file(file_path):
        try:
            file = open(file_path, "r")
            contents = file.readlines()
            file.close()
            contents = [x.rstrip() for x in contents]
            return contents
        except Exception:
            print("Could not read file " + file_path)


    @staticmethod
    def retrieve_all_folders_in_directory(parent_directory):
        folders = [o for o in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, o))]
        if '@eaDir' in folders:
            folders.remove("@eaDir")
        return folders


    @staticmethod 
    def retrieve_all_files_in_directory(directory):
        files = [f for f in listdir(directory) if isfile(join(directory, f))]
        files = OsUtils.clear_macos_system_files(files)
        return files


    @staticmethod
    def does_directory_exist(dir):
        return os.path.isdir(dir)


    @staticmethod
    def does_file_exist(file):
        return os.path.isfile(file)


    @staticmethod 
    def retrieve_directory_from_file_path(file_path):
        return os.path.dirname(file_path)


    @staticmethod
    def rename_file(original_name, new_name):
        os.rename(original_name, new_name)


    @staticmethod
    def rename_directory(original_name, new_name):
        os.rename(original_name, new_name)


    @staticmethod
    def clear_macos_system_files(file_list):
        if ".DS_Store" in file_list:
            file_list.remove(".DS_Store")
        return file_list


    @staticmethod
    def convert_relative_to_absolute_file_path(relative_file_path):
        return os.path.abspath(relative_file_path)


    @staticmethod
    def extract_file_name_from_full_directory_path(file_path):
        return os.path.basename(file_path)


    @staticmethod
    def extract_file_name_without_ext_from_full_directory_path(file_path):
        file_name_with_ext = OsUtils.extract_file_name_from_full_directory_path(file_path)
        return os.path.splitext(file_name_with_ext)[0]


    @staticmethod 
    def extract_directory_from_full_file_path(file_path):
        return os.path.dirname(os.path.abspath(file_path))


    @staticmethod
    def extract_current_folder_from_directory_path(directory_path):
        """"E.g. an input of /folderA/folderB/folderC/folderD/' will give you an output of 'folderD"""
        return os.path.basename(os.path.normpath(directory_path))


    @staticmethod
    def delete_file(file_path):
        os.remove(file_path)


    def delete_folder_and_contents(file_path):
        try:
            rmtree(file_path)
            
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))


    @staticmethod
    def copy_file(src, dst):
        copyfile(src, dst)