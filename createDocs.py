from __future__ import print_function
from saveAndExport import saveAndExport
import os, sys
#import ia_tools

#This script will 
#Save the project and export the plc open xml to the same path as the .project file
project = projects.primary
filePath = saveAndExport(project, '-p')

if filePath != None:
    #Calculate the file path of the docs folder
    docsPath = os.path.join(os.path.dirname(filePath), 'docs')

    #Set the format to iecMd for the first version
    format = 'iecMd'

    #Call an external python script that will generate the documentation (Python3 and ia_tools must be installed)
    #proj = ia_tools.Project(filepath)
    print(docsPath, format)
else:
    print('Doc generation failed, xml file not generated')
    


