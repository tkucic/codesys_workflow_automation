#Codesys iron python / python 2.7
from __future__ import print_function
from saveAndExport import saveAndExport
import os, sys, subprocess

#This script will 
#Save the project and export the plc open xml to the same path as the .project file
project = projects.primary
filePath = saveAndExport(project, '-p')

if filePath != None:
    #Calculate the file path of the docs folder
    savePath = os.path.join(os.path.dirname(filePath), 'docs')

    #Set the format based on arguments
    print(sys.argv)
    try:
        if sys.argv[1] in ['html', 'iecMd', 'md', 'iec']:
            format = sys.argv[1]

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
                    print('Doc generation failed, failed to execute call_ia_tools.py')
                else:
                    print('Documentation generated succesfully')
            else:
                print('Doc generation failed, call_ia_tools.py script not found in ScriptCommands')

    except IndexError:
        print('Doc generation failed, export format argument missing or unsupported')

else:
    print('Doc generation failed, xml file not generated')
    


