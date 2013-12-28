import maya
maya.utils.loadStringResourcesForModule(__name__)

import zlib
import zipfile
import maya.cmds as cmds

def pyError(errorString):
	""" print an error message """
	import maya.mel as mel
	try:
		mel.eval('error "%s"' % errorString)
	except: pass

def pyResult(resultString):
	""" print a result message """
	import maya.mel as mel
	msg = maya.stringTable['y_zipScene.kResult']  % resultString
	mel.eval('print "%s"' % msg)

def zipManyFiles(files):
	fileName = maya.cmds.file(q=True, sceneName=True)
	# If the scene has not been saved
	if (fileName==""):
		pyError( maya.stringTable['y_zipScene.kSceneNotSavedError']   )
		return

	# If the scene has been created, saved and then erased from the disk 
	elif (maya.cmds.file(q=True, exists=True)==0):
		msg = maya.stringTable['y_zipScene.kNonexistentFileError']  % fileName
		pyError(msg) 
		return

	# get the default character encoding of the system
	theLocale = cmds.about(codeset=True)

	# get a list of all the files associated with the scene
	# files = maya.cmds.file(query=1, list=1, withoutCopyNumber=1)
	
	# create a zip file named the same as the scene by appending .zip 
	# to the name
	zipFileName = (files[0])+'.zip'
	zip=zipfile.ZipFile(zipFileName, 'w', zipfile.ZIP_DEFLATED)

	# add each file associated with the scene, including the scene
	# to the .zip file
	for file in files:
		name = file.encode(theLocale)
		zip.write(name)		
	zip.close()

	# output a message whose result is the name of the zip file newly created
	pyResult(zipFileName)