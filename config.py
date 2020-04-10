# Python imports
import inspect
import os
import shutil


# Class used for directory handling
class Directory:

    def __init__(self, folder, file):
        # Get script directory
        name = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(name))

        # Set directories
        self.dir = path + '/' + folder
        self.file = path + '/' + folder + '/' + file
        self.name = [folder, file]

    # Change directory
    def change(self):
        os.chdir(self.dir)

    # Make folder
    def make(self):
        os.mkdir(self.dir, 0o777)

    # Delete directory contents
    def delete(self):
        shutil.rmtree(self.dir)

    # Test if directory is a file
    def is_file(self):
        return os.path.isfile(self.file)

    # Test if directory is a folder
    def is_folder(self):
        return os.path.isdir(self.dir)


# Tell the user they have ran the wrong .py file
def main():
    print('Please run python main.py not' + __file__)
    exit(0)


# We've all seen this before :P
if __name__ == "__main__":
    main()
