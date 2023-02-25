# Python Website Generation

## project_page_generation.py
This utility generates HTML files with images based on a template.  The purpose of this utility is to generate project picture pages without a bunch of manual pages for each project.  Instead, your data can be entered into the JSON file, which is much faster.  This also allows for easy updates of both the project pages and the template when desired.

The utility looks in all subfolders for an image.json file that contains data about the page that should be generated.  It also looks for all png, jpg, and jpeg files in that subfolder to include in the page.  Each generated HTML is placed in the search directory.

#### To Do:
- [ ] Move to object from dictionary for page details
- [ ] Add a sample HTML template





###### **All code, projects, and samples have no warranty expressed or implied. Code samples have the ability to overwrite output files. Code is meant for education and evaluation purposes only. Sample data should be used.
