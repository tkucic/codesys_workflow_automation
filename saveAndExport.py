from __future__ import print_function
import os, sys

#Select the current active project. The one its open in codesys
project = projects.primary

if project != None:
    #Save project
    project.save()
    print('Saved project')

    #Calculate the projects name based on path
    proj_name = os.path.basename(project.path).split('.')[0]

    #Calculate the new file name
    fpath = os.path.join(os.path.dirname(project.path), proj_name + '.xml')

    #Check if a flag has been passed
    try:
        if sys.argv[1] in ['-p', '--plcopenxml']:
            project.export_xml(project.get_children(recursive=True), path=fpath, recursive=True, export_folder_structure=True)
            print('Exported plcOpenXml to ', fpath)

        elif sys.argv[1] in ['-n', '--nativexml']:
            #Export to native codesys xml
            project.export_native(destination=fpath, recursive=True, profile_name=None, reporter=None)
            print('Exported Native Xml to ', fpath)

    except IndexError:
        #Export to PLCOpenXML
        project.export_xml(project.get_children(recursive=True), path=fpath, recursive=True, export_folder_structure=True)
        print('Exported plcOpenXml to ', fpath)
else:
    print('Error - No project open')


