import os
import shutil
import json
import datetime

def main():
    #Get directory and check status
    
    output_directory = input("Please enter the output directory: ")
    if os.path.isdir(output_directory) == False:
        print(f"{output_directory} is not a directory.")
        exit(0)

    #Get all subdirectories
    subdirectory_list = GetAllSubdirectories(output_directory)
    pertinent_subdirectory_list = []
    for x in subdirectory_list:
        json_filename = os.path.join(x, "images.json")
        if os.path.exists(json_filename):
            #Get data and add to dictionary if a valid JSON is found
            if os.path.isfile(json_filename):
                tempdict = {}
                tempdict["root"] = output_directory
                tempdict["relative"] = os.path.relpath(x,output_directory)
                file = open(json_filename)
                json_file_data = json.load(file)
                tempdict.update(json_file_data)

                #Fill in any gaps
                if "short_title" not in tempdict:
                    tempdict["short_title"] = "Temp Title"

                if "long_title" not in tempdict:
                    tempdict["long_title"] = "Temporary Page Title"

               
                file.close()
                pertinent_subdirectory_list.append(tempdict)

    pass

    #Pulling this into memory isn't incredibly efficient, but the files are small.
    #All data is stored in the dictionary at this point
    for current_subdirectory in pertinent_subdirectory_list:
        template_file = open(os.path.join(output_directory,"project_page_template.html"),"rt")
        output_file = open(os.path.join(output_directory,current_subdirectory["html_filename"]), "w")
        template_content = template_file.readlines()
        template_file.close()
        output_content = []
        for current_line in template_content:
            temp_line = current_line

            #Set current date/time to deal with PITA CSS caching
            now = datetime.datetime.utcnow()
            temp_line = temp_line.replace("%%css%%", now.strftime('%m%d%y%H%M%S'))

            #Short title instances
            temp_line = temp_line.replace("%%short_title%%", current_subdirectory["short_title"])

            #Long title instances
            temp_line = temp_line.replace("%%long_title%%", current_subdirectory["long_title"])


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
    
def GetAllSubdirectories(passed_path:str):
    #We only care about directories here
    return_list = []
    for root in os.walk(passed_path):
        return_list.append(root[0])
    return return_list

#Keep at bottom
if __name__ == "__main__":
    main()