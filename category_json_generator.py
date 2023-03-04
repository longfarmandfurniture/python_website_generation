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
                temp_page["page_data_file"] = os.path.relpath(json_filename, output_directory)

                #Just get data needed.  Another script will get the rest of the information.
                page_list.append(temp_page)

    #Get list of parent pages
    parent_page_list = []
    for x in page_list:
        parent_page_file = x["parent_page"]
        #Add dict if it doesn't exist
        #if parent_page_file not in parent_page_list:
        if parent_page_file not in [i['parent_page'] for i in parent_page_list]:
            print(f"Adding parent page {parent_page_file}")
            temp_page = {}
            temp_page["parent_page"] = parent_page_file
            #Add sample values that the user will modify later
            temp_page["short_title"] = "Taskbar Title"
            temp_page["long_title"] = "Longer Title for Page Content"
            temp_page["description"] = ["Description list", "Add as desired"]
            temp_page["preview_file_name"] = "1200x630ImageFileForShare"
            #Add list of jsons, user will rearrange to desired order.
            temp_page["json_data_file_list"] = [x["page_data_file"]]
            
            

            parent_page_list.append(temp_page)
        #Add data if parent page already in list
        else:
            temp_list = []
            #Not that efficient, but this is a utility script for a small number of files
            for current_page in parent_page_list:
                temp_dict = {}
                if current_page["parent_page"] == parent_page_file:
                    temp_dict = current_page
                    temp_dict["json_data_file_list"].append(x["page_data_file"])
                temp_list.append(temp_dict)
            parent_page_list = temp_list

            pass
            #Find a good way to do this with list comprehension.  
            #Need to add value to list in dict that matches.  

    for current_page in parent_page_list:
        #Write output JSON
        #We write to a separated file so that the user-modified file isn't overwritten.
        filename = current_page["parent_page"].replace(".html","") + "_automated" + ".json"
        output_file = open(os.path.join(output_directory,filename), "w")
        print(f"Writing output json file {output_file.name}")
        json.dump(current_page, output_file, indent=4)
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