#Codesys iron python / python 2.7
from __future__ import print_function
from interfaceLib import saveAndExport
import os, subprocess

#This script will 
#Save the project and export the plc open xml to the same path as the .project file
project = projects.primary
filePath = saveAndExport(project, '-p')

if filePath == None:
    raise Exception('Project xml not generated')

#Calculate the file path of the docs folder
savePath = os.path.join(os.path.dirname(filePath), 'docs')

#Set the format based on config
#Choose from['html', 'iecMd', 'md', 'iec']
format = 'iecMd'

if format in ['html', 'iecMd', 'md', 'iec']:
    
    #Call an external python script that will generate the documentation (Python3 and ia_tools must be installed)
    ia_toolsScriptLocation = os.path.join(os.path.dirname(__file__), 'call_ia_tools.py')
    
    #Check if the call_ia_tools.py exists
    if os.path.isfile(ia_toolsScriptLocation):
        cmd = ['python', 
            ia_toolsScriptLocation,
            filePath,
            savePath,
            format]
        if subprocess.call(cmd) != 0:
            raise Exception('Execution of call_ia_tools.py failed')
        else:
            print('Documentation generated succesfully')
    else:
        raise Exception('Script call_ia_tools.py not installed')
else:
    raise Exception('Invalid documentation format')




