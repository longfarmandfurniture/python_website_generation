import os
import shutil
import json
import datetime

def main():
    #Get directory and check status
    input_directory = input("Please enter the input directory: ")
    if os.path.isdir(input_directory) == False:
        print(f"{input_directory} is not a directory.")
        exit(0)

    output_directory = input("Please enter the output directory: ")
    if os.path.isdir(output_directory) == False:
        print(f"{output_directory} is not a directory.")
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

    #Get JSON data
    if os.path.exists(json_file_name):
        if os.path.isfile(json_file_name):
            file = open(json_file_name)
            json_file_data = json.load(file)
            html_filename = RetrieveFromJson(json_file_data, "html_filename")
            short_title = RetrieveFromJson(json_file_data, "short_title")
            long_title = RetrieveFromJson(json_file_data, "long_title")

    #Pulling this into memory isn't incredibly efficient, but the files are small.
    template_file = open(os.path.join(output_directory,"project_page_template.html"),"rt")
    output_file = open(os.path.join(output_directory,html_filename), "w")
    template_content = template_file.readlines()
    template_file.close()
    output_content = []
    for current_line in template_content:
        temp_line = current_line

        #Set current date/time to deal with PITA CSS caching
        now = datetime.datetime.utcnow()
        temp_line = temp_line.replace("%%css%%", now.strftime('%m%d%y%H%M%S'))

        #Short title instances
        temp_line = temp_line.replace("%%short_title%%", short_title)

        #Long title instances
        temp_line = temp_line.replace("%%long_title%%", long_title)


        #append line to output list
        output_content.append(temp_line)

    output_file.writelines(output_content)
    output_file.close()
    pass









def RetrieveFromJson(passed_json:dict, passed_index_name:str):
    if passed_index_name in passed_json:
        return passed_json[passed_index_name]
    else:
        return None

#Keep at bottom
if __name__ == "__main__":
    main()