from __future__ import print_function
import os, sys

def saveAndExport(project, arg):
    """Saves and exports the project to the xml type provided in the argument
    Args : 
        '-p', '-plcopenxml' -> PLC OpenXml format
        '-n', '--nativexml' -> Codesys native format
    The xml file is saved as the project name in the same folder as the .project file"""

    if project != None:
        #Save project
        project.save()
        print('Saved project')

        #Calculate the projects name based on path
        proj_name = os.path.basename(project.path).split('.')[0]

        #Calculate the new file name
        fpath = os.path.join(os.path.dirname(project.path), proj_name + '.xml')

        if arg in ['-p', '--plcopenxml']:
            #Export to PLCOpenXML
            project.export_xml(project.get_children(recursive=True), path=fpath, recursive=True, export_folder_structure=True)
            print('Exported plcOpenXml to ', fpath)

        elif arg in ['-n', '--nativexml']:
            #Export to native codesys xml
            project.export_native(destination=fpath, recursive=True, profile_name=None, reporter=None)
            print('Exported Native Xml to ', fpath)
        #Return the saved file path
        return fpath
    else:
        print('Error - No project open')
        return None

if __name__=='__main__':
    #Check if a flag has been passed
    try:
        if sys.argv[1] in ['-p', '--plcopenxml']:
            #Export to PLCOpenXML
            saveAndExport(projects.primary, '-p')

        elif sys.argv[1] in ['-n', '--nativexml']:
            #Export to native codesys xml
            saveAndExport(projects.primary, '-n')

    except IndexError:
        #Export to PLCOpenXML
        saveAndExport(projects.primary, '-p')
