from codesysBulker import CodesysBulker

if __name__=='__main__':
    project = CodesysBulker(projects.primary)
    print('Saving and exporting to native Codesys Xml')
    fPath = project.saveAndExport('-n')
    print('Exported to: ', fPath)
