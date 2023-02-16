from codesysBulker import CodesysBulker

if __name__=='__main__':
    project = CodesysBulker(projects.primary)
    print('Saving and exporting to PLCOpenXML')
    fPath = project.saveAndExport('-p')
    print('Exported to: ', fPath)