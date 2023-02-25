import os
import json

def main():
    output_directory = input("Please enter the output directory: ")
    if os.path.isdir(output_directory) == False:
        print(f"{output_directory} is not a directory.")
        exit(0)

    #Get all subdirectories
    subdirectory_list = GetAllSubdirectories(output_directory)
    page_list = []

    for x in subdirectory_list:
        json_filename = os.path.join(x, "images.json")
        if os.path.exists(json_filename):
            #Get data and add to dictionary if a valid JSON is found
            if os.path.isfile(json_filename):
                print(f"Found file {json_filename}.")
                tempdict = {}
                tempdict["root"] = output_directory
                tempdict["relative"] = os.path.relpath(x,output_directory)
                file = open(json_filename)
                json_file_data = json.load(file)
                tempdict.update(json_file_data)
                file.close()

                temp_page = {}
                temp_page["parent_page"] = tempdict["parent_page"]
                temp_page["page_data_file"] = json_filename

                #Just get data needed.  Another script will get the rest of the information.
                page_list.append(temp_page)

    #Get list of parent pages
    parent_page_list = []
    for x in page_list:
        parent_page_file = x["parent_page"]
        #Add dict if it doesn't exist
        if parent_page_file not in parent_page_list:
            print(f"Adding parent page {parent_page_file}")
            temp_page = {}
            temp_page["parent_page"] = parent_page_file
            parent_page_list.append(temp_page)
            

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