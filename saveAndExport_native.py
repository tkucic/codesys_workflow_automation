from interfaceLib import saveAndExport

if __name__=='__main__':
    print('Saving and exporting to native Codesys Xml')
    fPath = saveAndExport(projects.primary, '-n')
    print('Exported to: ', fPath)
