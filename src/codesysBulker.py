# Python 2.7
# IronPython
from __future__ import print_function
#Codesys script engine, located by default at C:\Program Files\CODESYS 3.5.18.20\CODESYS\ScriptLib\Stubs
import scriptengine
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
    '2db5746d-d284-4425-9f7f-2663a34b0ebc' : 'DT',
    '8ac092e5-3128-4e26-9e7e-11016c6684f2' : 'Action',
    'f8a58466-d7f6-439f-bbb8-d4600e41d099' : 'Method',
    '738bea1e-99bb-4f04-90bb-a7a567e74e3a' : 'Folder',
    '6f9dac99-8de1-4efc-8465-68ac443b7d08' : 'POU',
    '085afe48-c5d8-4ea5-ab0d-b35701fa6009' : 'Project Information',
    '8e687a04-7ca7-42d3-be06-fcbda676c5ef' : '__VisualizationStyle',
    '413e2a7d-adb1-4d2c-be29-6ae6e4fab820' : 'Call to POU'
}
class CodesysUIInterface:
    def __init__(self, selectedProject, verbose = False):
        '''Takes in the selected Codesys project. E.g. CodesysUIInterface(project.primary)'''
        if selectedProject == None:
            raise Exception('Project argument invalid')

        self.project = selectedProject
        self.verbose = verbose

        self.app = None
        self.onlineApp = None

        return
    def setIpOnGateway(self, gateway, ipaddress):
        '''Sets the IP address on the gateway communication on the PLC'''
        return NotImplementedError

    def build(self):
        '''Builds the active application'''
        if self.app == None:
            self.app = self.project.active_application
        
        self.app.build()
    
    def generate_app_code(self):
        '''Generates code for the active application'''
        if self.app == None:
            self.app = self.project.active_application
        
        self.app.generate_code()

    def create_online_application(self):
        '''Creates and online application e.g for going online'''
        self.onlineApp = scriptengine.online.create_online_application()

    def login(self, changeOption = 1):
        '''Goes online with the active application.
        changeOption:
            Never   = 0 Online change shall never be performed. In that case a full download is forced.  
            Try     = 1 Online change shall be tried. If not possible, a full download shall be performed.  
            Force   = 2 Online change shall be forced. If not possible, the action is terminated with no change.  
            Keep    = 3 Try to login. Do not online update. Do not download. Keep as it is.  
        '''
        if self.onlineApp == None:
            self.create_online_application()

        self.onlineApp.login(changeOption, False)

    def logout(self):
        '''Logs out of the application'''
        if self.onlineApp.IsLoggedIn:
            self.onlineApp.logout()
        else:
            print('Already logged out')

    def startApp(self):
        '''Starts the active application if logged in'''
        if self.onlineApp.IsLoggedIn:
            self.onlineApp.start()
        else:
            print('Start app failed. Not logged in.')

    def stopApp(self):
        '''Stops the active application if logged in'''
        if self.onlineApp.IsLoggedIn:
            self.onlineApp.stop()
        else:
            print('Stop app failed. Not logged in.')
            
class CodesysBulker:
    def __init__(self, selectedProject, verbose = False):
        '''Takes in the selected Codesys project. E.g. CodesysBulker(project.primary)'''
        if selectedProject == None:
            raise Exception('Project argument invalid')

        self.project = selectedProject
        self.verbose = verbose

        #Get the projects name and directory based on path
        self.proj_name = os.path.basename(self.project.path).split('.')[0]
        self.proj_dir  = os.path.dirname(self.project.path)

        #Get the names and types of all objects found in the project for future use
        self.proj_objects = {
            'folders' : [],
            'pous' : [],
            'dts' : [],
            'other' : []
        }
        if self.verbose:
            print('Getting list of objects')
        self.getListOfObjects(self.project)

        return

    def getListOfObjects(self, node):
        '''Returns a list of dictionaries of all objects found in the project.
        format: {'name' : 'fbExy', 'type' : 'function'}'''
        if node.is_root:
            self.proj_objects['other'].append({
                'name' : node.path,
                'type' : 'root'
            })
        else:
            guid = str(node.type)
            if guid in GUIDS.keys():
                #We are interested only in POUs and Data types as they must be unique
                if GUIDS[guid] == 'POU':
                    self.proj_objects['pous'].append(node.get_name(False))
                elif GUIDS[guid] == 'DT':
                    self.proj_objects['dts'].append(node.get_name(False))
                else:
                    self.proj_objects['other'].append({
                    'name' : node.get_name(False),
                    'type' : GUIDS[guid]
                    })
            else:
                self.proj_objects['other'].append({
                    'name' : node.get_name(False),
                    'type' : 'GUID: ' + str(node.type)
                })
        #Continue the search until the bottom
        for child in node.get_children(recursive = False):
            self.getListOfObjects(child)

    def saveAndExport(self, arg):
        """Saves and exports the project to the xml type provided in the argument
        Args : 
            '-p', '-plcopenxml' -> PLC OpenXml format
            '-n', '--nativexml' -> Codesys native format
        The xml file is saved as the project name in the same folder as the .project file"""

        #If no argument passed
        if arg not in ['-p', '--plcopenxml', '-n', '--nativexml']:
            raise Exception('Invalid format argument')

        #Save project if unsaved
        if self.project.dirty:
            self.project.save()

        #Calculate the new file name
        fpath = os.path.join(self.proj_dir, self.proj_name + '.xml')

        if arg in ['-p', '--plcopenxml']:
            if self.verbose:
                print('Saving PLCOpenXml to: ', fpath)
            #Export to PLCOpenXML
            self.project.export_xml(self.project.get_children(recursive=True), path=fpath, recursive=True, export_folder_structure=True)
            #Return the saved file path
            return fpath

        if arg in ['-n', '--nativexml']:
            if self.verbose:
                print('Saving Native Xml to: ', fpath)
            #Export to native codesys xml
            self.project.export_native(objects=self.project.get_children(recursive=True), destination=fpath, recursive=True, profile_name=None, reporter=None)
            #Return the saved file path
            return fpath
        return ''

    def createFolder(self, name, root=None):
        """Creates a folder under the provided root and returns its handler class.
        If the folder already exists then it returns its handler. If there is multiple folders with the same name it returns the first.
        If the root argument is passed in then it tries to place the folder under that object
        Raises exception if the folder was unable to be created"""
        if root == None:
            root = self.project

        #Check if it exists first under this namespace
        #Folders can be as nested as they want to be, 
        # as long we dont try to create a folder with the 
        # same name on the same level
        found = root.find(name, recursive = False)
        if found:
            if self.verbose:
                print('Folder ', name, ' already exists')
                return found[0]
        else:
            #Folder doesnt exists, create a new folder
            if self.verbose:
                print('Creating folder ', name)
            root.create_folder(name)
        
        #Find the newly created folder and return its handler (root.create_folder doesnt return the handler unfortunately)
        return root.find(name, recursive = False)[0]

    def addDut(self, dt, root=None):
        """Creates a datatype inside of the root codesys object(folder). Takes in a dictionary in correct format
        If the root argument is passed in then it tries to place the folder under that object
        If the object with the same name exists, it will update it"""
        if root == None:
            root = self.project
        
        #Take a look if it exists
        if dt.get('name') in self.proj_objects['dts']:
            self._updateDut(root.find(dt.get('name'), recursive=True)[0], dt)
            return

        self._createDut(dt, root = root)

    def _updateDut(self, existingDt, newDt):
        '''Updates and existing data type with the data found in newDt argument.
        newDt argument requires specific dictionary keys. Check documentation...lol'''
        if self.verbose:
            print('Updating data type ', newDt.get('name'))

        #Update the dt
        try:
            #Write the declaration
            existingDt.textual_declaration.replace(self._createDtDecl(newDt))

        except Exception as e:
            print('Update failed: ', e)

    def _createDut(self, dt, root=None):
        """Creates a datatype inside of the root codesys object(folder). Takes in a dictionary in correct format
        If the root argument is passed in then it tries to place the folder under that object"""
        if self.verbose:
            print('Creating data type ', dt.get('name'))
        #Create the data type
        try:
            crpFct = root.create_dut(dt.get('name'))

            #Write the declaration
            crpFct.textual_declaration.replace(self._createDtDecl(dt))

        except Exception as e:
            print('Import failed: ', e)

    def addPou(self, pou, root=None):
        """Creates a POU inside of the root codesys object(folder). Takes in a dictionary in correct format
        If the root argument is passed in then it tries to place the folder under that object
        If the object with the same name exists, it will update it"""
        if root == None:
            root = self.project
        
        #Take a look if it exists
        if pou.get('name') in self.proj_objects['pous']:
            for object in root.find(pou.get('name'), recursive=True):
                if GUIDS.get(object.type) != 'Call to POU':
                    self._updatePou(object, pou)
                    return
            else:
                raise Exception('POU location determination failed')

        self._createPou(pou, root = root)

    def _updatePou(self, existingPou, newPou):
        '''Updates and existing POU with the data found in newPou argument.
        newPou argument requires specific dictionary keys. Check documentation...lol'''
        if self.verbose:
            print('Updating POU ', newPou.get('name'))
        try:
            #Write the declaration and the code
            existingPou.textual_declaration.replace(self._createPouDecl(newPou))
            existingPou.textual_implementation.replace(newPou.get('code', ''))

            #Create actions if any
            for action in newPou.get('actions'):
                for child in existingPou.get_children():
                    if child.get_name() == action.get('name'):
                        if self.verbose:
                            print('Updating ', newPou.get('name'),'.',action.get('name'))
                        child.textual_implementation.replace(action.get('code', ''))
                        break
                else:
                    if self.verbose:
                        print('Creating ', newPou.get('name'),'.',action.get('name'))
                    act = existingPou.create_action(name=action.get('name'))
                    act.textual_implementation.replace(action.get('code', ''))

            #Create methods if any
            for method in newPou.get('methods'):
                for child in existingPou.get_children():
                    if child.get_name() == method.get('name'):
                        if self.verbose:
                            print('Updating ', newPou.get('name'),'.',method.get('name'))
                        child.textual_declaration.replace(self._createMethodDecl(method))
                        child.textual_implementation.replace(method.get('code', ''))
                        break
                else:
                    if self.verbose:
                        print('Creating ', newPou.get('name'),'.',method.get('name'))
                    met = existingPou.create_method(name=method.get('name'))
                    met.textual_declaration.replace(self._createMethodDecl(method))
                    met.textual_implementation.replace(method.get('code', ''))

        except Exception as e:
            print('Update failed: ', e)

    def _createPou(self, pou, root=None):
        """Creates a pou inside of the root codesys object(folder). Takes in a dictionary in correct format
        If the root argument is passed in then it tries to place the folder under that object"""
        if root == None:
            root = self.project
            
        #Create the pou
        if self.verbose:
            print('Creating ', pou.get('type'), ' ', pou.get('name'))
        try:
            if pou.get('type') == 'function':
                crpFct = root.create_pou(name=pou.get('name'), type=scriptengine.PouType.Function, return_type=pou.get('returnType'))
            elif pou.get('type') == 'program':
                crpFct = root.create_pou(name=pou.get('name'), type=scriptengine.PouType.Program)
            elif pou.get('type') == 'functionBlock':
                crpFct = root.create_pou(name=pou.get('name'), type=scriptengine.PouType.FunctionBlock)
                
            #Write the declaration and the code
            crpFct.textual_declaration.replace(self._createPouDecl(pou))
            crpFct.textual_implementation.replace(pou.get('code', ''))

            #Skip if this is a function as it cannot have methods or actions
            if pou.get('type') == 'function':
                return

            #Create actions if any
            for action in pou.get('actions'):
                if self.verbose:
                    print('Creating ', pou.get('name'), '.', action.get('name'))
                act = crpFct.create_action(name=action.get('name'))
                act.textual_implementation.replace(action.get('code', ''))

            #Create methods if any
            for method in pou.get('methods'):
                if self.verbose:
                    print('Creating ', pou.get('name'), '.', method.get('name'))
                met = crpFct.create_method(name=method.get('name'))
                met.textual_declaration.replace(self._createMethodDecl(method))
                met.textual_implementation.replace(method.get('code', ''))

        except Exception as e:
            print('Import failed: ', e)

    def _createPouDecl(self, pou):
        """Returns a string representing the declaration field that can be used for direct import to codesys"""
        decl = ''

        #Assemble description of the POU
        if pou.get('description') not in [None, '']:
            decl += '(*' + pou.get('description') + '*)\n'
        if pou.get('docLink') not in ['', None]:
            decl += '(*Docs: ' + pou.get('docLink') + '*)\n'

        #Assemble POU identifier
        if pou.get('type') == 'function':
            decl += 'FUNCTION ' + pou.get('name') + ' : ' + pou.get('returnType')+'\n'
        elif pou.get('type') == 'functionBlock':
            decl += 'FUNCTION_BLOCK ' + pou.get('name')+'\n'
        elif pou.get('type') == 'program':
            decl += 'PROGRAM ' + pou.get('name')+'\n'

        #Assemble variable/parameter interface
        for varBlock in pou.get('if'):
            decl += varBlock.get('name') + ' ' + varBlock.get('attribute').upper() + '\n'
            for var in varBlock.get('vars'):
                decl += "\t{0} : {1}{2}; {3}\n".format(
                    var.get('name'),
                    var.get('type'),
                    ' := '+ var.get('initialValue') if var.get('initialValue') not in [None, ''] else '',
                    '(*'+ var.get('description') + '*)' if var.get('description') not in [None, ''] else '')
            decl += 'END_VAR\n'
        return decl

    def _createMethodDecl(self, pou):
        """Returns a string representing the declaration field that can be used for direct import to codesys"""
        decl = ''

        #Assemble description of the POU
        if pou.get('description') not in [None, '']:
            decl += '(*' + pou.get('description') + '*)\n'
        if pou.get('docLink') not in ['', None]:
            decl += '(*Docs: ' + pou.get('docLink') + '*)\n'

        #Assemble POU identifier
        if pou.get('returnType') == None:
            decl += 'METHOD ' + pou.get('name') +'\n'
        else:
            decl += 'METHOD ' + pou.get('name') + ' : ' + pou.get('returnType')+'\n'

        #Assemble variable/parameter interface
        for varBlock in pou.get('if'):
            decl += varBlock.get('name') + '\n'
            for var in varBlock.get('vars'):
                decl += "\t{0} : {1}{2}; {3}\n".format(
                    var.get('name'),
                    var.get('type'),
                    ' := '+ var.get('initialValue') if var.get('initialValue') not in [None, ''] else '',
                    '(*'+ var.get('description') + '*)' if var.get('description') not in [None, ''] else '')
            decl += 'END_VAR\n'
        return decl

    def _createDtDecl(self, dt):
        """Returns a string representing the declaration field that can be used for direct import to codesys"""
        decl = ''
        #Assemble description of the POU
        if dt.get('description') not in [None, '']:
            decl += "(*{0}*)\n".format(dt.get('description'))
        if dt.get('docLink') not in ['', None]:
            decl += "(*Docs: {0}*)\n".format(dt.get('docLink'))

        #Main body
        decl += "TYPE " + dt.get('name') +  ':\n'
        if dt.get('baseType') == 'struct':
            decl += "STRUCT\n"
            for cpt in dt.get('components'):
                decl += "\t{0} : {1}{2}; {3}\n".format(
                    cpt.get('name'),
                    cpt.get('type'),
                    ' := '+ cpt.get('initialValue') if cpt.get('initialValue') not in [None, ''] else '',
                    '(*'+ cpt.get('description') + '*)' if cpt.get('description') not in [None, ''] else '')
            decl += "END_STRUCT\n"
        elif dt.get('baseType') == 'enum':
            decl += '(\n'
            for cpt in dt.get('components'):
                decl += "\t{0}{1}{2},\n".format(
                    cpt.get('name'),
                    ' := '+ cpt.get('initialValue') if cpt.get('initialValue') not in [None, ''] else '',
                    '(*'+ cpt.get('description') + '*)' if cpt.get('description') not in [None, ''] else '')
            #Remove the second to last character (,) from the last line
            decl = decl[:-2]
            decl += '\n);\n'
        decl += "END_TYPE"

        return decl
