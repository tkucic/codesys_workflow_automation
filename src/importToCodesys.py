from codesysBulker import CodesysBulker
import json, datetime, os

if __name__ == '__main__':

    #Log times for profiling execution
    startTime = datetime.datetime.now()
    times = []

    #Load data from the json file that is next to this script
    tempTime = datetime.datetime.now()
    print(str(datetime.datetime.now()), ': Load data from external file')
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'data.json'), 'r') as f:
        data = json.loads(f.read())
    times.append(('Time to load the external file ',datetime.datetime.now()-tempTime))

    #Get the bulker handle
    project = CodesysBulker(projects.primary, True)

    #Create namespaces and the objects
    for ns in data.get('namespaces'):
        tempTime = datetime.datetime.now()
        #Create the folder that holds the namespaces objects
        nsFolder = project.createFolder(ns.get('name'))

        #Create POUs of the namespace
        for pouType in ['fcs', 'fbs', 'prgs']:
            for pou in ns.get(pouType):
                project.addPou(pou, nsFolder)
        
        #Create data types
        for dt in ns.get('dts'):
            project.addDut(dt, nsFolder)

        #Create global variables
        #Not implemented
        times.append(('Time to create namespace ' + ns.get('name'), datetime.datetime.now()-tempTime))

    tempTime = datetime.datetime.now()
    times.append(('Time to create data types ',datetime.datetime.now()-tempTime))

    #Print the times of execution
    for time in times:
        print(time[0], str(time[1]))
    print('Total script time: ', str(datetime.datetime.now() - startTime))