#!/usr/bin/env python
from DIRAC.Core.Base import Script
Script.parseCommandLine(ignoreErrors=False)

from DIRAC.Core.DISET.RPCClient import RPCClient

simpleMessageService = RPCClient('dips://besdirac02.ihep.ac.cn:62222/DataManagement/SimpleMessage')

result = simpleMessageService.getMessage()

if not result['OK']:
  print "Error while calling the service:", result['Message']
else:
  for k, v in result['Values'].items():
    print k, v
