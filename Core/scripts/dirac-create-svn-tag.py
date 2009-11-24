#!/usr/bin/env python
# $HeadURL$
"""
Tag a new release in SVN
"""
__RCSID__ = "$Id$"
from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Base      import Script
from DIRAC.Core.Utilities import List, CFG

import sys, os, tempfile, shutil, getpass, subprocess

svnProjects = 'DIRAC'
svnVersions = ""

svnSshRoot    = "svn+ssh://%s@svn.cern.ch/reps/dirac/%s"

def setVersion( optionValue ):
  global svnVersions
  svnVersions = optionValue
  return S_OK()

def setProject( optionValue ):
  global svnProjects
  svnProjects = optionValue
  return S_OK()

Script.disableCS()

Script.registerSwitch( "v:", "version=",                "versions to tag comma separated (mandatory)", setVersion )
Script.registerSwitch( "p:", "project=",                "projects to tag comma separated (default = DIRAC)", setProject )

Script.parseCommandLine( ignoreErrors = False )

gLogger.info( 'Executing: %s ' % ( ' '.join(sys.argv) ) )

def usage():
  Script.showHelp()
  exit(2)
  
if not svnVersions:
  usage()

def getSVNFileContents( projectName, filePath ):
  import urllib2, stat
  gLogger.info( "Reading %s/trunk/%s" % ( projectName, filePath ) ) 
  viewSVNLocation = "http://svnweb.cern.ch/world/wsvn/dirac/%s/trunk/%s?op=dl&rev=0" % ( projectName, filePath )
  anonymousLocation = 'http://svnweb.cern.ch/guest/dirac/%s/trunk/%s' % ( projectName, filePath )
  downOK = False
  for remoteLocation in ( viewSVNLocation, anonymousLocation ):
    try:
      remoteFile = urllib2.urlopen( remoteLocation )
    except urllib2.URLError:
      gLogger.exception()
      continue
    remoteData = remoteFile.read()
    remoteFile.close()      
    return remoteData
  if not downOK:
    p = subprocess.Popen( "svn cat 'http://svnweb.cern.ch/guest/dirac/%s/trunk/%s'" % ( projectName, filePath ), 
                          shell = True, stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE, close_fds = True )
    remoteData = p.stdout.read().strip()
    p.wait()
    if not remoteData:
      print "Error: Could not retrieve %s from the web nor via SVN. Aborting..." % fileName
      sys.exit(1)
  return remoteData
#End of helper functions

#Get username
userName = raw_input( "SVN User Name[%s]: " % getpass.getuser() )
if not userName:
  userName = getpass.getuser()

#Start the magic!
for svnProject in List.fromChar( svnProjects ):
    
  versionsData = getSVNFileContents( svnProject, "%s/versions.cfg" % svnProject )
  
  buildCFG = CFG.CFG().loadFromBuffer( versionsData )
  
  if 'Versions' not in buildCFG.listSections():
    gLogger.error( "versions.cfg file in project %s does not contain a Versions top section" % svnProject )
    continue

  for svnVersion in List.fromChar( svnVersions ):
    
    gLogger.info( "Start tagging for project %s version %s " %  ( svnProject, svnVersion ) )
    if not svnVersion in buildCFG[ 'Versions' ].listSections():
      gLogger.error( 'Version does not exist:', svnVersion )
      gLogger.error( 'Available versions:', ', '.join( buildCFG.listSections() ) )
      continue
  
    versionCFG = buildCFG[ 'Versions' ][svnVersion]
    packageList = versionCFG.listOptions()
    gLogger.info( "Tagging packages: %s" % ", ".join( packageList ) )
    msg = '"Release %s"' % svnVersion
    dest = svnSshRoot % ( userName, '%s/tags/%s/%s_%s/%s' % ( svnProject, svnProject, svnProject, svnVersion, svnProject ) )
    cmd = 'svn --parents -m %s mkdir %s' % ( msg, dest )
    source = []
    for extra in buildCFG.getOption( 'rootPackageFiles', ['__init__.py', 'versions.cfg'] ):
      source.append( svnSshRoot % ( userName, '%s/trunk/%s/%s'  % ( svnProject, svnProject, extra ) ) )
    for pack in packageList:
      packVer = versionCFG.getOption(pack,'')
      if packVer in ['trunk', '', 'HEAD']:
        source.append( svnSshRoot % ( userName, '%s/trunk/%s/%s'  % ( svnProject, svnProject, pack ) ) )
      else:
        source.append( svnSshRoot % ( userName, '%s/tags/%s/%s/%s' % ( svnProject, svnProject, pack, packVer ) ) )
    if not source:
      gLogger.error( 'No packages to be included' )
      exit( -1 )
    gLogger.info( 'Creating SVN Dir:', dest )
    ret = os.system( cmd )
    if ret:
      exit( -1 )
    gLogger.info( 'Copying packages: %s' % ", ".join( packageList ) )
    cmd = 'svn -m %s copy %s %s' % ( msg, ' '.join( source ), dest )
    ret = os.system( cmd )
    if ret:
      gLogger.error( 'Failed to create tag' )


  