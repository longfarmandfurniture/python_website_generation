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
    project_list = []
    for x in subdirectory_list:
        json_filename = os.path.join(x, "images.json")
        if os.path.exists(json_filename):
            #Get data and add to dictionary if a valid JSON is found
            if os.path.isfile(json_filename):
                print(f"Found file: {json_filename}.")
                tempdict = {}
                tempdict["root"] = output_directory
                tempdict["relative"] = os.path.relpath(x,output_directory)
                file = open(json_filename)
                json_file_data = json.load(file)
                tempdict.update(json_file_data)

                #Get picture filenames, relative path, but OS dependent
                images_list = FindFilesRelative(output_directory, x, "jpg,jpeg,png")
                images_list.sort()
                tempdict["image_paths"] = images_list
                pass
                #Preview image, not included with files
                #return [i for i, x in enumerate(lst) if x<a or x>b]
                if "preview_file_name" in tempdict:
                    temp_index = [i for i, x in enumerate(images_list) if x.endswith(tempdict["preview_file_name"])]
                    if len(temp_index) > 0:
                        tempdict["preview_file_location"] = images_list[temp_index[0]]
                        images_list.remove(images_list[temp_index[0]])
                        print(f"Found preview image {tempdict['preview_file_name']}.")
                    pass

                #Fill in any gaps
                if "short_title" not in tempdict:
                    tempdict["short_title"] = "Temp Title"

                if "long_title" not in tempdict:
                    tempdict["long_title"] = "Temporary Page Title"

                if "description" not in tempdict:
                    tempdict["description"] = [ "Temporary description." ]

               
                file.close()
                project_list.append(tempdict)

    pass

    #Pulling this into memory isn't incredibly efficient, but the files are small.
    #All data is stored in the dictionary at this point
    for current_project in project_list:
        template_file = open(os.path.join(output_directory,"zz_project_page_template.html"),"rt")
        output_file = open(os.path.join(output_directory,current_project["html_filename"]), "w")
        template_content = template_file.readlines()
        template_file.close()
        output_content = []
        for current_line in template_content:
            append_line = True
            temp_line = current_line

            #Set current date/time to deal with PITA CSS caching
            now = datetime.datetime.utcnow()
            temp_line = temp_line.replace("%%css%%", now.strftime('%m%d%y%H%M%S'))

            #Short title instances
            temp_line = temp_line.replace("%%short_title%%", current_project["short_title"])

            #Long title instances
            temp_line = temp_line.replace("%%long_title%%", current_project["long_title"])

            #Meta description tag
            temp_line = temp_line.replace("%%meta_description%%", current_project["meta_description"])

            #Preview/thumbnail
            if "preview_file_location" in current_project:
                temp_line = temp_line.replace("%%preview%%", current_project["preview_file_location"].replace("\\", "/"))

            #Return link
            temp_line = temp_line.replace("%%parent%%", current_project["parent_page"])

            #Page filename
            temp_line = temp_line.replace("%%html_filename%%", current_project["html_filename"])

            #Variable number of description lines
            if "%%description%%" in temp_line:
                append_line = False
                for item in current_project["description"]:
                    output_content.append(f"\t\t{item}\n<br><br>\n")

                #Add link to build or finished pages if they exist.  Defined in JSON
                if "build_page" in current_project:
                    if current_project["build_page"] != "":
                        output_content.append(f"\t\t<a href=\"{current_project['build_page']}\">Click here to see the build!</a>\n<br><br>\n")

                if "finished_page" in current_project:
                    if current_project["finished_page"] != "":
                        output_content.append(f"\t\t<a href=\"{current_project['finished_page']}\">Click here to see the finished project!</a>\n<br><br>\n")

                #Add link to previous page if it exists.  Defined in JSON
                if "previous_page" in current_project:
                    if current_project["previous_page"] != "":
                       output_content.append(f"\t\t<a href=\"{current_project['previous_page']}\">Click here to see the previous page for this project.</a>\n<br><br>\n")

               #Add link to next page if it exists.  Defined in JSON
                if "next_page" in current_project:
                    if current_project["next_page"] != "":
                       output_content.append(f"\t\t<a href=\"{current_project['next_page']}\">Click here to see the next page for this project.</a>\n<br><br>\n")


            if "%%images%%" in temp_line:
                append_line = False
                for current_image in current_project["image_paths"]:
                    #For HTML since source dict will be OS dependent
                    image_file_name = os.path.basename(current_image)
                    html_path = current_image.replace("\\", "/")

                    nodata = True
                    if "images" in current_project:
                        if image_file_name in current_project["images"]:
                            output_content.append(f"\t\t<img src=\"{html_path}\" alt=\"{current_project['images'][image_file_name]}\"><br><br>\n")
                            nodata = False
                    if nodata:
                        output_content.append(f"\t\t<img src=\"{html_path}\"><br><br>\n")

            pass

            #append line to output list
            if append_line:
                output_content.append(temp_line)
        print(f"Writing file: {current_project['html_filename']}.")
        output_file.writelines(output_content)
        output_file.close()
    pass







def FindFilesRelative(passed_root: str, passed_directory:str, passed_extensions:str):
    extension_list = passed_extensions.split(",")
    file_list = os.listdir(passed_directory)
    
    return_list = []
    for file in file_list:
        for extension in extension_list:
            if file.lower().endswith(extension.replace(" ", "").lower()):
                relative_path = os.path.relpath(passed_directory, passed_root)
                return_list.append(os.path.join(relative_path,file))
    return return_list

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