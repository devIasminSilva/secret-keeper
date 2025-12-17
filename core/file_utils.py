import shutil
import os

class FileUtils:
    @staticmethod
    def zip_folder(folder_path: str) -> str:
        """Zips a folder and returns the path to the zip file."""
        zip_path = shutil.make_archive(folder_path, 'zip', folder_path)
        return zip_path

    @staticmethod
    def cleanup_file(path: str):
        """Removes a file if it exists."""
        if os.path.exists(path):
            os.remove(path)
