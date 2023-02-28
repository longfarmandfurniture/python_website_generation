import os
import shutil
import json
import datetime


def main():
    # Get directory and check status
    output_directory = input("Please enter the output directory: ")
    if os.path.isdir(output_directory) == False:
        print(f"{output_directory} is not a directory.")
        exit(0)

    #get all JSON files in output directory
    json_files = []
    for file in os.listdir(output_directory):
        if file.endswith(".json"):
            #Only grab user-modified version
            if not "automated.json" in file:
                json_files.append(file)

    category_list = []
    for current_json_file in json_files:
        full_json_path = os.path.join(output_directory,current_json_file)
        if os.path.exists(full_json_path):
             # Get data and add to dictionary if a valid JSON is found
             if os.path.isfile(full_json_path):
                print(f"Found file: {current_json_file}")
                #Did it this way in case I need to add any data here
                tempdict = {}
                file = open(full_json_path)
                json_file_data = json.load(file)
                file.close()
                tempdict.update(json_file_data)
                category_list.append(tempdict)


    # Pulling this into memory isn't incredibly efficient, but the files are small.
    # Some data is stored in dictionaries, but dictionaries have links to json files for project pages
    for current_category in category_list:
        template_file = open(os.path.join(output_directory,"category_page_template.html"), "rt")
        output_file = open(os.path.join(output_directory, current_category["parent_page"]), "w")
        #Get template content
        template_content = template_file.readlines()
        template_file.close
        pass


    pass







    #     output_content = []
    #     for current_line in template_content:
    #         append_line = True
    #         temp_line = current_line

    #         # Set current date/time to deal with PITA CSS caching
    #         now = datetime.datetime.utcnow()
    #         temp_line = temp_line.replace(
    #             "%%css%%", now.strftime('%m%d%y%H%M%S'))

    #         # Short title instances
    #         temp_line = temp_line.replace(
    #             "%%short_title%%", current_project["short_title"])

    #         # Long title instances
    #         temp_line = temp_line.replace(
    #             "%%long_title%%", current_project["long_title"])

    #         # Preview/thumbnail
    #         temp_line = temp_line.replace(
    #             "%%preview%%", current_project["preview_file_location"].replace("\\", "/"))

    #         # Return link
    #         temp_line = temp_line.replace(
    #             "%%parent%%", current_project["parent_page"])

    #         # Variable number of description lines
    #         if "%%description%%" in temp_line:
    #             append_line = False
    #             for item in current_project["description"]:
    #                 output_content.append(f"\t\t{item}\n<br><br>\n")

    #         if "%%images%%" in temp_line:
    #             append_line = False
    #             for current_image in current_project["images"]:
    #                 # For HTML since source dict will be OS dependent
    #                 html_path = current_image.replace("\\", "/")
    #                 output_content.append(
    #                     f"\t\t<img src=\"{html_path}\"><br><br>\n")

    #         # append line to output list
    #         if append_line:
    #             output_content.append(temp_line)
    #     print(f"Writing file: {current_project['html_filename']}.")
    #     output_file.writelines(output_content)
    #     output_file.close()
    # pass


















def RetrieveFromJson(passed_json: dict, passed_index_name: str):
    if passed_index_name in passed_json:
        return passed_json[passed_index_name]
    else:
        return None


# Keep at bottom
if __name__ == "__main__":
    main()
