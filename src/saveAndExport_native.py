# Python 2.7
# IronPython
#Codesys script engine, located by default at C:\Program Files\CODESYS 3.5.18.20\CODESYS\ScriptLib\Stubs
import scriptengine

from codesysBulker import CodesysBulker

if __name__=='__main__':
    project = CodesysBulker(scriptengine.projects.primary)
    print('Saving and exporting to native Codesys Xml')
    fPath = project.saveAndExport('-n')
    print('Exported to: ', fPath)
