# Workflow automation scripts for CODESYS

Collection of scripts meant for Codesys that automate workflow inside of the IDE.

## Available scripts

### Save project and export to xml

This script will save your active project and export all of its objects in wanted format. Supported formats are PLC Open Xml and Codesys native Xml. The resulting file will be exported to the same folder the active project is located. This script must be run from CODESYS by its script engine.
Due to a bug in CODESYS script parameters(arguments) cannot be passed to the script if ran from the UI so two separate scripts are created just to pass in arguments.

* saveAndExport_plcopenxml.py for PLC Open Xml

* saveAndExport_native.py for Codesys Native Xml

![screenshot of the script buttons](toolbarExample.png)

## Installation

### Manual installation

* Create the Script Commands folder in one of the storage locations. I recommend C:\ProgramData\CODESYS\Script Commands

* Copy the Python, config.json and the .ico files there.

* Start CODESYS. The script files, configuration file, and symbol files are read and provided in the Tools -> Customize dialog in the Command Icons tab, ScriptEngine Commands category. Add the scripts to wanted shortcuts

More on codesys scripting on [Codesys Online Help](https://help.codesys.com/webapp/_cds_struct_using_scripts;product=codesys;version=3.5.16.0)

### Automatic build script

In the repo I have provided the build.py script that can be ran and it will install all necessary scripts, icons and config.json to the C:\ProgramData\CODESYS\Script Commands folder. In case the folder already exists, the script will update the config.json and update the scripts that have the same name as in the new config.json. If you have scripts of your own already mapped to config.json, they will not be overwritten if they have a different name. Automatic build must be ran with administrative rights. If you have a problem with that, the build script is python so you can read what it does, or you can always install manually.

## License

MIT

## Contribution

Raise a pull request with the modified config.json, icons and the script if you want to add some useful scripts to the project.
 