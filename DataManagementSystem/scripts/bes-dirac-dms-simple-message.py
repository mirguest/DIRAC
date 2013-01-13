#!/usr/bin/env python
from DIRAC.Core.Base import Script
Script.parseCommandLine(ignoreErrors=False)

from DIRAC.Core.DISET.RPCClient import RPCClient

simpleMessageService = RPCClient('dips://besdirac02.ihep.ac.cn:62222/DataManagement/SimpleMessage')
#simpleMessageService = RPCClient('dips://besdirac02.ihep.ac.cn:62222/Framework/SimpleMessage')
#simpleMessageService = RPCClient('dips://besdirac02.ihep.ac.cn:42222/Framework/SimpleMessage')
#simpleMessageService = RPCClient('dips://besdirac02.ihep.ac.cn:32222/Accounting/SimpleMessage')

result = simpleMessageService.getMessage()

print result

if not result['OK']:
  print "Error while calling the service:", result['Message']
else:
  for k, v in result['Value'].items():
    print k, v
