# Python 3.9
import os, json, shutil
# Builds the necessary scripts and places them in Script Commands
# If Script commands already exists, it updates the config.json and installs new scripts, updates old ones

# Define some paths
remRootPath = r'C:\ProgramData\CODESYS\Script Commands'
remConfigPath = os.path.join(remRootPath,'config.json')
locConfigPath = os.path.join(os.getcwd(), 'config.json')
locSrcPath = os.path.join(os.getcwd(), 'src')
locRespath = os.path.join(os.getcwd(), 'res')

#Check if C:\ProgramData\CODESYS\Script Commands exists, if not create it
os.makedirs(remRootPath, exist_ok=True)

#Load local config.json
with open(locConfigPath, 'r') as f:
    localCfgs = json.loads(f.read())

#Check if config.json exists
if os.path.isfile(remConfigPath):
    print('config.json existing, updating...')
    #If it exists, we cannot overwrite existing config, we can only add or update
    with open(remConfigPath, 'r') as f:
        #File can be empty or invalid json, we need to check
        #Read the file and convert it back to dictionary
        remCfgs = json.loads(f.read())

    #Update the dictionary with new data
    for localCfg in localCfgs:
        for remCfg in remCfgs:
            if localCfg.get('Name') == remCfg.get('Name'):
                #Update the remCfg with new data
                remCfg = localCfg
                break
        else:
            #Script not found, add it
            remCfgs.append(localCfg)

    #Now when eveyrything is updated, save it back
    json.dump(remCfgs, open(remConfigPath, 'w' ), indent=2)
    print('config.json updated')
else:
    print('config.json doesnt exists, creating new...')
    #The config.json doesnt exist so we just write local config to the new file
    json.dump(localCfgs, open(remConfigPath, 'w' ), indent=2)
    print('config.json created')

#Now we need to move the .py files from src folder to script commands
for root, dirs, files in os.walk(locSrcPath):
    for file in files:
        ret = shutil.copy(os.path.join(locSrcPath, file), remRootPath)
        print('Exported script to: ', ret)

#Now we need to move the icon files from res to the script commands
for root, dirs, files in os.walk(locSrcPath):
    for file in files:
        ret = shutil.copy(os.path.join(locSrcPath, file), remRootPath)
        print('Exported resource to: ', ret)

print('Build completed')