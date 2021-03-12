from interfaceLib import saveAndExport

if __name__=='__main__':
    print('Saving and exporting to PLCOpenXML')
    fPath = saveAndExport(projects.primary, '-p')
    print('Exported to: ', fPath)