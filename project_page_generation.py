import os
import shutil
import json

def main():
    #Get directory and check status
    input_directory = input("Please enter the input directory: ")
    if os.path.isdir(input_directory) == False:
        print(f"{input_directory} is not a directory.")
        exit(0)

    #Check for images object 
    json_file_data = None
    json_file_name = os.path.join(input_directory, "images.json")
    
    #Output filename
    html_filename = None

    #Tab title
    short_title = None

    #Header title
    long_title = None

    if os.path.exists(json_file_name):
        if os.path.isfile(json_file_name):
            file = open(json_file_name)
            json_file_data = json.load(file)
            html_filename = RetrieveFromJson(json_file_data, "html_filename")
            short_title = RetrieveFromJson(json_file_data, "short_title")
            long_title = RetrieveFromJson(json_file_data, "long_title")


    pass









def RetrieveFromJson(passed_json:dict, passed_index_name:str):
    if passed_index_name in passed_json:
        return passed_json[passed_index_name]
    else:
        return None

#Keep at bottom
if __name__ == "__main__":
    main()