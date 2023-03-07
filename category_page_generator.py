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
        template_file = open(os.path.join(output_directory,"zz_category_page_template.html"), "rt")
        output_file = open(os.path.join(output_directory, current_category["parent_page"]), "w")
        #Get template content
        template_content = template_file.readlines()
        template_file.close

        #modified page content lines
        output_content = []

        for current_line in template_content:
            append_line = True

            #Set current date/time to deal with PITA CSS caching
            now = datetime.datetime.utcnow()
            current_line = current_line.replace("%%css%%", now.strftime('%m%d%y%H%M%S'))

            #Short title instances
            current_line = current_line.replace("%%short_title%%", current_category["short_title"])

            #Long title instances
            current_line = current_line.replace("%%long_title%%", current_category["long_title"])

            #Meta description tag
            current_line = current_line.replace("%%meta_description%%", current_category["meta_description"])

            #Parent page
            current_line = current_line.replace("%%parent%%", current_category["parent_page"])

            #Variable number of description lines
            if "%%description%%" in current_line:
                append_line = False
                for item in current_category["description"]:
                    output_content.append(f"\t\t{item}\n<br><br>\n")

        
            if "%%project_links%%" in current_line:
                append_line = False

                #Here we're getting the JSON file from the individual project page so we can get data there
                for current_json_data_file in current_category["json_data_file_list"]:
                    json_full_path = os.path.join(output_directory, current_json_data_file)
                    if os.path.isfile(json_full_path):
                        print(f"Found file: {json_full_path}")
                        tempdict = {}
                        with open(json_full_path) as file:
                            tempdict = json.load(file)
                        
                        #Create link/image in page from share link (should always be share size)
                        output_content.append(f'\t\t<a href="{tempdict["html_filename"]}">')
                        preview_file_path = os.path.relpath(os.path.dirname(json_full_path), output_directory) + f"/{tempdict['preview_file_name']}"
                        #for Windows
                        preview_file_path = preview_file_path.replace("\\", "/")
                        if "preview_alt_text" in tempdict:
                            output_content.append(f"<img src=\"{preview_file_path}\" alt=\"{tempdict['preview_alt_text']}\">")
                        else:
                            output_content.append(f"<img src=\"{preview_file_path}\">")
                        output_content.append(f'</a><br><br>\n')


            #append line to output list
            if append_line:
                output_content.append(current_line)


        print(f"Writing file: {current_category['parent_page']}.")
        output_file.writelines(output_content)
        output_file.close()        
        
        pass


    pass

def RetrieveFromJson(passed_json: dict, passed_index_name: str):
    if passed_index_name in passed_json:
        return passed_json[passed_index_name]
    else:
        return None


# Keep at bottom
if __name__ == "__main__":
    main()
