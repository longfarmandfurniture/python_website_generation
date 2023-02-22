import os
import shutil
import json

def main():
    #Get directory and check status
    input_directory = input("Please enter the input directory: ")
    if os.path.isdir(input_directory) == False:
        print(f"{input_directory} is not a directory.")
        exit(0)















#Keep at bottom
if __name__ == "__main__":
    main()