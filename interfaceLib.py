from __future__ import print_function
from scriptengine import * #If codesys must import this module, this has to be here
import os

def saveAndExport(project, arg):
    """Saves and exports the project to the xml type provided in the argument
    Args : 
        '-p', '-plcopenxml' -> PLC OpenXml format
        '-n', '--nativexml' -> Codesys native format
    The xml file is saved as the project name in the same folder as the .project file"""

    if project == None:
        raise Exception('Project argument invalid')
    
    #Save project if unsave
    if project.dirty:
        project.save()

    #Calculate the projects name based on path
    proj_name = os.path.basename(project.path).split('.')[0]

    #Calculate the new file name
    fpath = os.path.join(os.path.dirname(project.path), proj_name + '.xml')

    if arg in ['-p', '--plcopenxml']:
        #Export to PLCOpenXML
        project.export_xml(project.get_children(recursive=True), path=fpath, recursive=True, export_folder_structure=True)
        #Return the saved file path
        return fpath

    elif arg in ['-n', '--nativexml']:
        #Export to native codesys xml
        project.export_native(objects=project.get_children(recursive=True), destination=fpath, recursive=True, profile_name=None, reporter=None)
        #Return the saved file path
        return fpath
    #If no argument passed
    raise Exception('Invalid format argument')
