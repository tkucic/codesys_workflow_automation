from __future__ import print_function
from scriptengine import * #If codesys must import this module, this has to be here
import os

#These guids serve as descriptors of existing objects inside of the project
GUIDS = {
    '8753fe6f-4a22-4320-8103-e553c4fc8e04' : 'Project Settings',
    '225bfe47-7336-4dbc-9419-4105a7c831fa' : 'Device',
    '40b404f9-e5dc-42c6-907f-c89f4a517386' : 'Plc Logic',
    '639b491f-5557-464c-af91-1471bac9f549' : 'Application',
    'adb5cb65-8e1d-4a00-b70a-375ea27582f3' : 'Library Manager',
    'ae1de277-a207-4a28-9efb-456c06bd52f3' : 'Task Configuration',
    '98a2708a-9b18-4f31-82ed-a1465b24fa2d' : 'Task',
    'ffbfa93a-b94d-45fc-a329-229860183b1d' : 'Global variable set',
    '2db5746d-d284-4425-9f7f-2663a34b0ebc' : 'data type',
    '8ac092e5-3128-4e26-9e7e-11016c6684f2' : 'action',
    '738bea1e-99bb-4f04-90bb-a7a567e74e3a' : 'Folder',
    '6f9dac99-8de1-4efc-8465-68ac443b7d08' : 'POU',
    '085afe48-c5d8-4ea5-ab0d-b35701fa6009' : 'Project Information',
    '8e687a04-7ca7-42d3-be06-fcbda676c5ef' : '__VisualizationStyle',
    '413e2a7d-adb1-4d2c-be29-6ae6e4fab820' : 'Call to POU'
}

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

    if arg in ['-p', '--plcopenxml']:
        
        #Calculate the new file name
        fpath = os.path.join(os.path.dirname(project.path), proj_name + '.xml')
        
        #Export to PLCOpenXML
        project.export_xml(project.get_children(recursive=True), path=fpath, recursive=True, export_folder_structure=True)
        
        #Return the saved file path
        return fpath

    elif arg in ['-n', '--nativexml']:
        
        #Calculate the new file name
        fpath = os.path.join(os.path.dirname(project.path), proj_name + '.export')
        
        #Export to native codesys xml
        project.export_native(objects=project.get_children(recursive=True), destination=fpath, recursive=True, profile_name=None, reporter=None)
        
        #Return the saved file path
        return fpath
    #If no argument passed
    raise Exception('Invalid format argument')

def createFolder(root, name):
    """Creates a folder inside of the CODESYS IDE and returns its handler class. If the folder already
    exists then it returns its handler. If there is multiple folders with the same name it returns the first"""
    
    #Check if it exists first
    print('Creating folder ', name)
    folders = root.find(name, recursive = True)
    for folder in folders:
        if folder.is_folder:
            print('Folder already exists')
            return folder
    else:
        #Folder doesnt exists, create a new folder
        root.create_folder(name)
    
    #Find the newly created folder and return its handler (root.create_folder doesnt return the handler unfortunately)
    folders = root.find(name, recursive = True)
    for folder in folders:
        if folder.is_folder:
            return folder
    else:
        raise Exception('Folder {1} couldnt be created'.format(name))

def updatePou(existingPou, newPou):
    #Update the pou
    try:
        #Write the declaration and the code
        existingPou.textual_declaration.replace(newPou.get('declaration', ''))
        existingPou.textual_implementation.replace(newPou.get('code', ''))

        #Create actions if any
        for action in newPou.get('actions'):
            for child in existingPou.get_children():
                if child.get_name() == action.get('name'):
                    child.textual_implementation.replace(action.get('code', ''))
                    break
            else:
                act = existingPou.create_action(name=action.get('name'))
                act.textual_implementation.replace(action.get('code', ''))

    except Exception as e:
        print('Update failed: ', e)

def updateDut(existingDt, newDt):
    #Update the dt
    try:
        #Write the declaration
        existingDt.textual_declaration.replace(newDt.get('declaration', ''))

    except Exception as e:
        print('Update failed: ', e)

def createDut(root, dt):
    """Creates a datatype inside of the root codesys object(folder). Takes in a dictionary in correct format"""

    #Create the pou
    try:
        crpFct = root.create_dut(dt.get('name'))

        #Write the declaration
        crpFct.textual_declaration.replace(dt.get('declaration', ''))

    except Exception as e:
        print('Import failed: ', e)

def createPou(root, pou):
    """Creates a pou inside of the root codesys object(folder). Takes in a dictionary in correct format"""

    #Create the pou
    try:
        if pou.get('type') == 'function':
            crpFct = root.create_pou(name=pou.get('name'), type=PouType.Function, return_type=pou.get('returnType'))
        elif pou.get('type') == 'program':
            crpFct = root.create_pou(name=pou.get('name'), type=PouType.Program)
        elif pou.get('type') == 'functionBlock':
            crpFct = root.create_pou(name=pou.get('name'), type=PouType.FunctionBlock)
            
        #Write the declaration and the code
        crpFct.textual_declaration.replace(pou.get('declaration', ''))
        crpFct.textual_implementation.replace(pou.get('code', ''))

        #Create actions and/or methods if any
        for action in pou.get('actions'):
            act = crpFct.create_action(name=action.get('name'))
            act.textual_implementation.replace(action.get('code', ''))

    except Exception as e:
        print('Import failed: ', e)
