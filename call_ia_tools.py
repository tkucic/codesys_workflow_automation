#python 3.9
import sys, os, ia_tools

xmlPath = sys.argv[1]
savePath = sys.argv[2]
format = sys.argv[3]
proj = ia_tools.Project(xmlPath)
proj.export(savePath, format)

