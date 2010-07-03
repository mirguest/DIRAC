""" UnitTest class for Client Commands classes
"""

import sys
import unittest
from datetime import datetime 

from DIRAC import S_OK, S_ERROR
import DIRAC.ResourceStatusSystem.test.fake_Logger
import DIRAC.ResourceStatusSystem.test.fake_Admin

from DIRAC.ResourceStatusSystem.Utilities.mock import Mock
from DIRAC.ResourceStatusSystem.Command.Command import Command
from DIRAC.ResourceStatusSystem.Command.MacroCommand import MacroCommand
from DIRAC.ResourceStatusSystem.Command.CommandCaller import CommandCaller
from DIRAC.ResourceStatusSystem.Command.ClientsInvoker import ClientsInvoker
from DIRAC.ResourceStatusSystem.Command.GOCDBStatus_Command import *
from DIRAC.ResourceStatusSystem.Command.Pilots_Command import *
from DIRAC.ResourceStatusSystem.Command.Jobs_Command import *
from DIRAC.ResourceStatusSystem.Command.SAMResults_Command import SAMResults_Command
from DIRAC.ResourceStatusSystem.Command.GGUSTickets_Command import *
from DIRAC.ResourceStatusSystem.Command.RS_Command import *
from DIRAC.ResourceStatusSystem.Command.DIRACAccounting_Command import *
from DIRAC.ResourceStatusSystem.Command.SLS_Command import *
from DIRAC.ResourceStatusSystem.Command.Collective_Command import *
#from DIRAC.ResourceStatusSystem.Client.SAMResultsClient import NoSAMTests
#from DIRAC.ResourceStatusSystem.Client.SLSClient import NoServiceException
from DIRAC.ResourceStatusSystem.Utilities.Exceptions import *
from DIRAC.ResourceStatusSystem.Utilities.Utils import *


#############################################################################

class ClientsCommandsTestCase(unittest.TestCase):
  """ Base class for the ClientsCommands test cases
  """
  def setUp(self):
    
    from DIRAC.Core.Base.Script import parseCommandLine
    parseCommandLine()

    sys.modules["DIRAC.Interfaces.API.DiracAdmin"] = DIRAC.ResourceStatusSystem.test.fake_Admin
#    sys.modules["DIRAC"] = DIRAC.ResourceStatusSystem.test.fake_Logger
    
    self.mock_command = Mock()
    self.mock_rsClient = Mock()
    self.mock_rsClient.getGeneralName.return_value = "LCG.Ferrara.it"
    
    self.co = Command()
    self.mco = MacroCommand()
    self.ci = ClientsInvoker()
    self.mock_client = Mock()
    self.mock_client_2 = Mock()
    self.GOCDBS_C = GOCDBStatus_Command()
    self.GOCDBI_C = GOCDBInfo_Command()
    self.PE_C = PilotsEff_Command()
    self.PS_C = PilotsStats_Command()
    self.JE_C = JobsEff_Command()
    self.JS_C = JobsStats_Command()
    self.SC_C = SystemCharge_Command()
    self.JES_C = JobsEffSimple_Command()
    self.JESC_C = JobsEffSimpleCached_Command()
    self.PES_C = PilotsEffSimple_Command()
    self.PESC_C = PilotsEffSimpleCached_Command()
    self.SAMR_C = SAMResults_Command()
    self.RSP_C = RSPeriods_Command()
    self.GGUS_O_C = GGUSTickets_Open()
    self.GGUS_L_C = GGUSTickets_Link()
    self.GGUS_I_C = GGUSTickets_Info()
    self.SeSt_C = ServiceStats_Command()
    self.ReSt_C = ResourceStats_Command()
    self.StElSt_C = StorageElementsStats_Command()
    self.MS_C = MonitoredStatus_Command()
    self.DQ_C = TransferQuality_Command()
    self.DA_C = DIRACAccounting_Command()
    self.SLSS_C = SLSStatus_Command()
    self.SLSSI_C = SLSServiceInfo_Command()
    self.SLSL_C = SLSLink_Command()
    self.JSEO_C = JobsEffSimpleEveryOne_Command()
    self.PSES_C = PilotsEffSimpleEverySites_Command()
    self.TQES_C = TransferQualityEverySEs_Command()
    self.TQC_C = TransferQualityCached_Command()
    self.DTES_C = DTEverySites_Command()
    self.DTER_C = DTEveryResources_Command()
    self.DTC_C = DTCached_Command()

    self.GOCDBS_C.setArgs(('Site', ))
    self.GOCDBI_C.setArgs(('Site', ))
    self.PE_C.setArgs(('Site', ))
    self.PS_C.setArgs(('Site', ))
    self.JE_C.setArgs(('Site', ))
    self.JS_C.setArgs(('Site', ))
    self.SC_C.setArgs(('Site', ))
    self.JES_C.setArgs(('Site', ))
    self.JESC_C.setArgs(('Site', ))
    self.PES_C.setArgs(('Site', ))
    self.PESC_C.setArgs(('Site', ))
    self.SAMR_C.setArgs(('Site', 'XX'))
    self.RSP_C.setArgs(('Site', ))
    self.GGUS_O_C.setArgs(('Site', ))
    self.GGUS_L_C.setArgs(('Site', ))
    self.GGUS_I_C.setArgs(('Site', ))
    self.SeSt_C.setArgs(('Site', ))
    self.ReSt_C.setArgs(('Site', ))
    self.StElSt_C.setArgs(('Site', ))
    self.MS_C.setArgs(('Site', ))
    self.DQ_C.setArgs(('Site', ))
    self.DA_C.setArgs(('Site', ))
    self.SLSS_C.setArgs(('Site', ))
    self.SLSSI_C.setArgs(('Site', ))
    self.SLSL_C.setArgs(('Site', ))
    self.JSEO_C.setArgs(('Site', ))
    self.PSES_C.setArgs(('Site', ))
    self.TQES_C.setArgs(('Site', ))
    self.TQC_C.setArgs(('Site', ))
    self.JSEO_C.setArgs(('Site', ))
    self.PSES_C.setArgs(('Site', ))
    self.TQES_C.setArgs(('Site', ))
    self.TQC_C.setArgs(('Site', ))

#############################################################################

class CommandSuccess(ClientsCommandsTestCase):

  def test_setArgs(self):
    for g in ValidRes:
      self.co.setArgs((g, 'XX'))
      self.assertEqual(self.co.args, (g, 'XX'))

#############################################################################

class CommandFailure(ClientsCommandsTestCase):

  def test_setBadArgs(self):
    self.failUnlessRaises(InvalidRes, self.co.setArgs, ('Sites', 'XX', 'Active'))
  

#############################################################################

class MacroCommandSuccess(ClientsCommandsTestCase):

  def test_setCommands(self):
    self.mco.setCommands(self.mock_command)
    self.assertEqual(self.mco.commands, [self.mock_command])

    self.mco.setCommands([self.mock_command, self.mock_command])
    self.assertEqual(self.mco.commands, [self.mock_command, self.mock_command])

#  def test_setArgs(self):
#    co = self.mock_command
#    self.mco.setCommands(co)
#    for g in ValidRes:
##      for a in ((g, 'XX'), [(g, 'XX'), (g, 'XX')]):
#      self.mco.setArgs((g, 'XX'))
#      self.assertEqual(self.mco.co.args, (g, 'XX'))

#############################################################################

class CommandCallerSuccess(ClientsCommandsTestCase):

  def test_setCommandObject(self):
    cc = CommandCaller()
    for comm in (('SAMResults_Command', 'SAMResults_Command'), 
                 ('GGUSTickets_Command', 'GGUSTickets_Open')):
      res = cc.setCommandObject(comm)
      self.assert_(type(res), Command)

#  def test_commandInvocation(self):
#    cc = CommandCaller()
#    for comm in (('SAMResults_Command', 'SAMResults_Command'), 
#                 ('GGUSTickets_Command', 'GGUSTickets_Open')):
#      res = cc.commandInvocation(comm = comm)

#############################################################################

class ClientsInvokerSuccess(ClientsCommandsTestCase):

  def test_setCommand(self):
    self.ci.setCommand(self.mock_command)
    self.assertEqual(self.ci.command, self.mock_command)

  def test_doCommand(self):
    self.mock_command.doCommand.return_value = {'DT': 'OUTAGE', 'Enddate': '2009-09-09 13:00:00'}
    self.ci.setCommand(self.mock_command)
    for granularity in ValidRes:
      res = self.ci.doCommand()
      self.assertEqual(res['DT'], 'OUTAGE')
    self.mock_command.doCommand.return_value = {'DT': 'AT_RISK', 'Enddate': '2009-09-09 13:00:00'}
    self.ci.setCommand(self.mock_command)
    for granularity in ValidRes:
      res = self.ci.doCommand()
      self.assertEqual(res['DT'], 'AT_RISK')
    self.mock_command.doCommand.return_value = None
    self.ci.setCommand(self.mock_command)
    for granularity in ValidRes:
      res = self.ci.doCommand()
      self.assertEqual(res, None)
        

#############################################################################

#class ClientsInvokerFailure(ClientsCommandsTestCase):
#  
#  def test_badArgs(self):
#    self.failUnlessRaises(Exception, self.ci.doCommand)
#    self.failUnlessRaises(Exception, self.ci.doCommand)
     
#############################################################################

class GOCDBStatus_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    now = datetime.utcnow().replace(microsecond = 0, second = 0)
    tomorrow = datetime.utcnow().replace(microsecond = 0, second = 0) + timedelta(hours = 24)
    inAWeek = datetime.utcnow().replace(microsecond = 0, second = 0) + timedelta(days = 7)
    
    nowLess12h = str( now - timedelta(hours = 12) )[:-3]
    nowPlus8h = str( now + timedelta(hours = 8) )[:-3]
    nowPlus24h = str( now + timedelta(hours = 24) )[:-3]
    nowPlus40h = str( now + timedelta(hours = 40) )[:-3]
    nowPlus50h = str( now + timedelta(hours = 50) )[:-3]
    nowPlus60h = str( now + timedelta(hours = 60) )[:-3]


    for granularity in ValidRes:
      args = (granularity, 'LCG.CERN.ch')
      for retVal in ( {'78305448': {'SITENAME': 'UKI-LT2-QMUL', 
                                   'FORMATED_END_DATE': nowPlus8h, 
                                   'SEVERITY': 'OUTAGE', 
                                   'FORMATED_START_DATE': nowLess12h, 
                                   'DESCRIPTION': 'Electrical work in the building housing the cluster.'} 
                      },
                      {'78305448': {'SITENAME': 'UKI-LT2-QMUL', 
                                   'FORMATED_END_DATE': nowPlus60h, 
                                   'SEVERITY': 'OUTAGE', 
                                   'FORMATED_START_DATE': nowPlus24h, 
                                   'DESCRIPTION': 'Electrical work in the building housing the cluster 1.'}, 
                      '78305449': {'SITENAME': 'UKI-LT2-QMUL', 
                                   'FORMATED_END_DATE': nowLess12h, 
                                   'SEVERITY': 'OUTAGE', 
                                   'FORMATED_START_DATE': nowPlus8h, 
                                   'DESCRIPTION': 'Electrical work in the building housing the cluster 2.'} 
                      },
                      {'78305448': {'SITENAME': 'UKI-LT2-QMUL', 
                                   'FORMATED_END_DATE': nowPlus60h, 
                                   'SEVERITY': 'OUTAGE', 
                                   'FORMATED_START_DATE': nowPlus50h,
                                   'DESCRIPTION': 'Electrical work in the building housing the cluster 1.'}, 
                      '78305449': {'SITENAME': 'UKI-LT2-QMUL', 
                                   'FORMATED_END_DATE': nowPlus24h, 
                                   'SEVERITY': 'OUTAGE', 
                                   'FORMATED_START_DATE': nowPlus8h, 
                                   'DESCRIPTION': 'Electrical work in the building housing the cluster 2.'} 
                      }
                    ):
        retVal = S_OK(retVal)
        self.mock_client.getStatus.return_value = retVal  
        self.GOCDBS_C.setArgs(args)
        self.GOCDBS_C.setClient(self.mock_client)
        res = self.GOCDBS_C.doCommand()
        self.assert_('OUTAGE' in res['Result']['DT'])
      self.mock_client.getStatus.return_value = {'OK':True, 
                                                 'Value':{'78305448': 
                                                          {'SITENAME': 'UKI-LT2-QMUL', 
                                                          'FORMATED_END_DATE': nowPlus40h, 
                                                          'SEVERITY': 'OUTAGE',
                                                          'FORMATED_START_DATE': nowPlus8h, 
                                                          'DESCRIPTION': 'Electrical work in the building housing the cluster.'} 
                                                 }}
      self.GOCDBS_C.setArgs(args)
      self.GOCDBS_C.setClient(self.mock_client)
      res = self.GOCDBS_C.doCommand()
      self.assertEqual(res['Result']['DT'], 'OUTAGE in 8 hours')
      self.mock_client.getStatus.return_value = {'OK':True, 
                                                 'Value':{'78305448': 
                                                          {'SITENAME': 'UKI-LT2-QMUL', 
                                                          'FORMATED_END_DATE': nowPlus40h, 
                                                          'SEVERITY': 'AT_RISK',
                                                          'FORMATED_START_DATE': nowPlus8h, 
                                                          'DESCRIPTION': 'Electrical work in the building housing the cluster.'}
                                                }} 
      res = self.GOCDBS_C.doCommand()
      self.assert_('AT_RISK' in res['Result']['DT'])
      self.mock_client.getStatus.return_value =  {'OK':True, 'Value': None}
      res = self.GOCDBS_C.doCommand()
      self.assertEqual(res['Result']['DT'], None)
      
#############################################################################

class GOCDBStatus_CommandFailure(ClientsCommandsTestCase):

  def test_badArgs(self):
    self.mock_client.getStatus.side_effect = RSSException
    self.GOCDBS_C.setArgs(('Site', 'LCG.CERN.ch'))
    self.GOCDBS_C.setClient(self.mock_client)
    res = self.GOCDBS_C.doCommand()
    self.assertEqual(res['Result'], 'Unknown')
      
  def test_badArgs(self):
    self.failUnlessRaises(InvalidRes, self.GOCDBS_C.setArgs, (('sites', '')))
     
#############################################################################

class GOCDBInfo_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    for granularity in ValidRes:
      args = (granularity, 'XX')
      self.mock_client.getInfo.return_value =  {'OK':True, 'Value': ['XXXX', 'YYYYYYYYY']}
      res = self.GOCDBI_C.doCommand(args, clientIn = self.mock_client)
      self.assertEqual(res, ['XXXX', 'YYYYYYYYY'])

#############################################################################

class GOCDBInfo_CommandFailure(ClientsCommandsTestCase):

  def test_badArgs(self):
    self.failUnlessRaises(InvalidRes, self.GOCDBI_C.doCommand, ('sites', ''))
    self.failUnlessRaises(TypeError, self.GOCDBI_C.doCommand, None)
     
#############################################################################

class Res2SiteStatus_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    for granularity in ValidRes:
      args = (granularity, 'XX')
      self.mock_client.getStatus.return_value =  {'OK':True, 'Value': {}}
      res = self.R2SS_C.doCommand(args, clientIn = self.mock_client)
      self.assertEqual()
      self.mock_client.getStatus.return_value = {'OK':True, 'Value': {}}
      res = self.R2SS_C.doCommand(args, clientIn = self.mock_client)
      self.assertEqual()
      self.mock_client.getStatus.return_value =  {'OK':True, 'Value': None}
      res = self.R2SS_C.doCommand(args, clientIn = self.mock_client)
      self.assertEqual(res, None)

#############################################################################
    

class Res2SiteStatus_CommandFailure(ClientsCommandsTestCase):

#  def test_clientFail(self):
#    self.mock_client.getStatus.side_effect = Exception()
#    for g in ValidRes:
#      res = self.PE_C.doCommand((g, 'XX', ['', '']), clientIn = self.mock_client)
#      self.assertEqual(res['PilotsEff'], 'Unknown')

  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.R2SS_C.doCommand, None)
     
#############################################################################

class PilotsEff_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    for granularity in ValidRes:
      args = (granularity, 'XX', ['', ''] )
      for pe in (0, 20, 40, 60, 80):
        self.mock_client.getPilotsEff.return_value =  pe
        self.PE_C.setArgs(args)
        self.PE_C.setClient(self.mock_client)
        res = self.PE_C.doCommand()
        self.assertEqual(res['Result'], pe)

#############################################################################
    

class PilotsEff_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getPilotsEff.side_effect = Exception()
    for g in ValidRes:
      for pe in (0, 20, 40, 60, 80):
        self.PE_C.setArgs((g, 'XX', ['', '']))
        self.PE_C.setClient(self.mock_client)
        res = self.PE_C.doCommand()
        self.assertEqual(res['Result'], 'Unknown')

  def test_badArgs(self):
    self.failUnlessRaises(InvalidRes, self.PE_C.setArgs, ('sites', '', []))
     
#############################################################################

class PilotsStats_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    for granularity in ValidRes:
      args = (granularity, 'XX', [])
      for pe in (0, 20, 40, 60, 80):
        self.mock_client.getPilotsStats.return_value =  pe
        self.PS_C.setArgs(args)
        self.PS_C.setClient(self.mock_client)
        res = self.PS_C.doCommand()
        self.assertEqual(res['Result'], pe)

#############################################################################

class PilotsStats_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getPilotsStats .side_effect = Exception()
    for g in ValidRes:
      for pe in (0, 20, 40, 60, 80):
        self.PS_C.setArgs((g, 'XX', []))
        self.PS_C.setClient(self.mock_client)
        res = self.PS_C.doCommand()
        self.assertEqual(res['Result'], 'Unknown')

  def test_badArgs(self):
    self.failUnlessRaises(InvalidRes, self.PS_C.setArgs, ('sites', '', []))
     
#############################################################################

class PilotsEffSimple_CommandSuccess(ClientsCommandsTestCase):

  def test_doCommand(self):

    args = ('Site', 'XX')
    for pe in ('Good', 'Fair', 'Poor', 'Bad', 'Idle'):
      self.mock_client.getPilotsSimpleEff.return_value = {'XX':pe}
      self.PES_C.setArgs(args)
      self.PES_C.setClient(self.mock_client)
      res = self.PES_C.doCommand()
      self.assertEqual(res['Result'], pe)

    mockRSC = Mock()
    mockRSC.getGeneralName.return_value = 'XX'
    args = ('Service', 'XX')
    for pe in ('Good', 'Fair', 'Poor', 'Bad', 'Idle'):
      self.mock_client.getPilotsSimpleEff.return_value = {'XX':pe}
      self.PES_C.setArgs(args)
      self.PES_C.setClient(self.mock_client)
      res = self.PES_C.doCommand(mockRSC)
      self.assertEqual(res['Result'], pe)

    mockRSC = Mock()
    mockRSC.getGeneralName.return_value = 'XX'
    args = ('Resource', 'XX')
    for pe in ('Good', 'Fair', 'Poor', 'Bad', 'Idle'):
      self.mock_client.getPilotsSimpleEff.return_value = {'XX':pe}
      self.PES_C.setArgs(args)
      self.PES_C.setClient(self.mock_client)
      res = self.PES_C.doCommand(mockRSC)
      self.assertEqual(res['Result'], pe)

#############################################################################
    
class PilotsEffSimple_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getPilotsSimpleEff.side_effect = Exception()
    for g in ('Site', 'Service', 'Resource'):
      for pe in ('Good', 'Fair', 'Poor', 'Bad', 'Idle'):
        self.PES_C.setArgs((g, 'XX'))
        self.PES_C.setClient(self.mock_client)
        res = self.PES_C.doCommand()
        self.assertEqual(res['Result'], 'Unknown')

  def test_badArgs(self):
    self.failUnlessRaises(InvalidRes, self.PES_C.setArgs, ('sites', ''))
     
#############################################################################

class JobsEff_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    for granularity in ValidRes:
      args = (granularity, 'XX', ['', ''] )
      for pe in (0, 20, 40, 60, 80):
        self.mock_client.getJobsEff.return_value = pe
        self.JE_C.setArgs(args)
        self.JE_C.setClient(self.mock_client)
        res = self.JE_C.doCommand()
        self.assertEqual(res['Result'], pe)

#############################################################################
    
class JobsEff_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getJobsEff .side_effect = Exception()
    for g in ValidRes:
      for pe in (0, 20, 40, 60, 80):
        self.JE_C.setArgs((g, 'XX', ['', '']))
        self.JE_C.setClient(self.mock_client)
        res = self.JE_C.doCommand()
        self.assertEqual(res['Result'], 'Unknown')

  def test_badArgs(self):
    self.failUnlessRaises(InvalidRes, self.JE_C.setArgs, ('sites', '', []))
     
#############################################################################

class JobsStats_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    for granularity in ValidRes:
      args = (granularity, 'XX', [])
      for pe in (0, 20, 40, 60, 80):
        self.mock_client.getJobsStats.return_value = pe
        self.JS_C.setArgs(args)
        self.JS_C.setClient(self.mock_client)
        res = self.JS_C.doCommand()
        self.assertEqual(res['Result'], pe)

#############################################################################
    
class JobsStats_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getJobsStats.side_effect = Exception()
    for g in ValidRes:
      for pe in ('Good', 'Fair', 'Poor', 'Bad', 'Idle'):
        self.JS_C.setArgs((g, 'XX'))
        self.JS_C.setClient(self.mock_client)
        res = self.JS_C.doCommand()
        self.assertEqual(res['Result'], 'Unknown')
    
  def test_badArgs(self):
    self.failUnlessRaises(InvalidRes, self.JS_C.setArgs, ('sites', '', []))
     
#############################################################################

#class SystemCharge_CommandSuccess(ClientsCommandsTestCase):
#  
#  def test_doCommand(self):
#
#    self.mock_client.getSystemCharge.return_value =  {'LastHour': 50, 'anHourBefore': 30}
#    res = self.SC_C.doCommand(clientIn = self.mock_client)
#    self.assertEqual(res['LastHour'], 50)
#    self.assertEqual(res['anHourBefore'], 30)
    
#############################################################################

class JobsEffSimple_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    args = ('Site', 'XX')
    for pe in ('Good', 'Fair', 'Poor', 'Bad', 'Idle'):
      self.mock_client.getJobsSimpleEff.return_value = {'XX':pe}
      self.JES_C.setArgs(args)
      self.JES_C.setClient(self.mock_client)
      res = self.JES_C.doCommand()
      self.assertEqual(res['Result'], pe)

    mockRSC = Mock()
    mockRSC.getGeneralName.return_value = 'XX'
    args = ('Service', 'XX')
    for pe in ('Good', 'Fair', 'Poor', 'Bad', 'Idle'):
      self.mock_client.getJobsSimpleEff.return_value = {'XX':pe}
      self.JES_C.setArgs(args)
      self.JES_C.setClient(self.mock_client)
      res = self.JES_C.doCommand(mockRSC)
      self.assertEqual(res['Result'], pe)

#############################################################################
   
class JobsEffSimple_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getJobsSimpleEff.side_effect = Exception()
    for g in ('Site', 'Service'):
      for pe in ('Good', 'Fair', 'Poor', 'Bad', 'Idle'):
        self.JES_C.setArgs((g, 'XX'))
        self.JES_C.setClient(self.mock_client)
        res = self.JES_C.doCommand()
        self.assertEqual(res['Result'], 'Unknown')
    
  def test_badArgs(self):
    self.failUnlessRaises(InvalidRes, self.JES_C.setArgs, ('sites', ''))
     
#############################################################################

class JobsEffSimpleCached_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    args = ('Site', 'XX')
    self.mock_client.getGeneralName.return_value = 'XX'
    for pe in ('Good', 'Fair', 'Poor', 'Bad', 'Idle'):
      self.mock_client.getCachedResult.return_value = (pe, )
      self.JESC_C.setArgs(args)
      self.JESC_C.setClient(self.mock_client)
      res = self.JESC_C.doCommand()
      self.assertEqual(res['Result'], pe)

#############################################################################
   
class JobsEffSimpleCached_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getCachedResult.side_effect = Exception()
    for g in ('Site', 'Service'):
      for pe in ('Good', 'Fair', 'Poor', 'Bad', 'Idle'):
        self.JESC_C.setArgs((g, 'XX'))
        self.JESC_C.setClient(self.mock_client)
        res = self.JESC_C.doCommand()
        self.assertEqual(res['Result'], 'Unknown')
    
  def test_badArgs(self):
    self.failUnlessRaises(InvalidRes, self.JESC_C.setArgs, ('sites', ''))
     
#############################################################################

class PilotsEffSimpleCached_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    args = ('Site', 'XX')
    for pe in ('Good', 'Fair', 'Poor', 'Bad', 'Idle'):
      self.mock_client.getCachedResult.return_value = (pe, )
      self.PESC_C.setArgs(args)
      self.PESC_C.setClient(self.mock_client)
      res = self.PESC_C.doCommand()
      self.assertEqual(res['Result'], pe)

#############################################################################
   
class PilotsEffSimpleCached_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getCachedResult.side_effect = Exception()
    for g in ('Site', 'Service'):
      for pe in ('Good', 'Fair', 'Poor', 'Bad', 'Idle'):
        self.PESC_C.setArgs((g, 'XX'))
        self.PESC_C.setClient(self.mock_client)
        res = self.PESC_C.doCommand()
        self.assertEqual(res['Result'], 'Unknown')
    
  def test_badArgs(self):
    self.failUnlessRaises(InvalidRes, self.PESC_C.setArgs, ('sites', ''))
     
#############################################################################

class SAMResults_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    for args in (('Site', 'LCG.CERN.ch'), ('Site', 'LCG.CERN.ch', 'CERN-PROD'), 
                 ('Resource', 'grid.fe.infn.it'), 
                 ('Resource', 'grid0.fe.infn.it', 'LCG.Ferrara.it'), 
                 ('Resource', 'grid0.fe.infn.it', None, ['aa', 'bbb']), 
                 ('Resource', 'grid0.fe.infn.it', 'LCG.Ferrara.it', ['aa', 'bbb'])):
      self.mock_client.getStatus.return_value =  {'OK':True, 
                                                  'Value': {'Status':None}}
      self.SAMR_C.setArgs(args)
      self.SAMR_C.setClient(self.mock_client)
      res = self.SAMR_C.doCommand(rsClientIn = self.mock_rsClient)
      self.assertEqual(res['Result'], {'Status':None})
      
    args = ('Resource', 'grid0.fe.infn.it', None, ['aa', 'bbb'])
    for status in ['ok', 'down', 'na', 'degraded', 'partial', 'maint']:
      self.mock_client.getStatus.return_value =  {'OK':True, 
                                                  'Value': {'Status':status}}
      self.SAMR_C.setArgs(args)
      self.SAMR_C.setClient(self.mock_client)
      res = self.SAMR_C.doCommand(rsClientIn = self.mock_rsClient)
      self.assertEqual(res['Result']['Status'], status)
    args = ('Resource', 'grid0.fe.infn.it', 'LCG.Ferrara.it', ['aa', 'bbb'])
    for status in ['ok', 'down', 'na', 'degraded', 'partial', 'maint']:
      self.mock_client.getStatus.return_value =  {'OK':True, 
                                                  'Value': {'Status':status}}
      self.SAMR_C.setArgs(args)
      self.SAMR_C.setClient(self.mock_client)
      res = self.SAMR_C.doCommand(rsClientIn = self.mock_rsClient)
      self.assertEqual(res['Result']['Status'], status)

#############################################################################

class SAMResults_CommandFailure(ClientsCommandsTestCase):

  def test_clientFail(self):
    self.mock_client.getStatus.side_effect = RSSException()
    for args in (('Site', 'LCG.CERN.ch'), ('Site', 'LCG.CERN.ch', 'CERN-PROD'), 
                 ('Resource', 'grid0.fe.infn.it'), ('Resource', 'grid0.fe.infn.it', 'LCG.Ferrara.it'), 
                 ('Resource', 'grid0.fe.infn.it', None, ['aa', 'bbb']), 
                 ('Resource', 'grid0.fe.infn.it', 'LCG.Ferrara.it', ['aa', 'bbb'])):
      self.SAMR_C.setArgs(args)
      self.SAMR_C.setClient(self.mock_client)
      res = self.SAMR_C.doCommand(rsClientIn = self.mock_rsClient)
      self.assertEqual(res['Result'], 'Unknown')
    
#    self.mock_client.getStatus.side_effect = NoSAMTests()
#    for args in (('Site', 'XX'), ('Site', 'XX', 'XXX'), 
#                 ('Resource', 'XX'), ('Resource', 'XX', 'XXX'), 
#                 ('Resource', 'grid0.fe.infn.it', None, ['aa', 'bbb']), 
#                 ('Resource', 'grid0.fe.infn.it', 'LCG.Ferrara.it', ['aa', 'bbb'])):
#      self.SAMR_C.setArgs(args)
#      self.SAMR_C.setClient(self.mock_client)
#      res = self.SAMR_C.doCommand(rsClientIn = self.mock_rsClient)
#      self.assertEqual(res['Result'], None)
    
  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.SAMR_C.setArgs, None)
     
#############################################################################

class GGUSTickets_Open_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    self.mock_client.getTicketsList.return_value = {'OK':True, 'Value': ({'terminal': 211, 'open': 2}, 
                                                    'https://gus.fzk.de/ws/ticket_search.php?')}
    self.GGUS_O_C.setArgs(('Site', 'LCG.CERN.ch'))
    self.GGUS_O_C.setClient(self.mock_client)
    res = self.GGUS_O_C.doCommand()
    self.assertEqual(res['Result'], 2)
    
#############################################################################

class GGUSTickets_All_CommandFailure(ClientsCommandsTestCase):

  def test_clientFail(self):
    self.mock_client.getTicketsList.side_effect = Exception()
    self.GGUS_O_C.setArgs(('Site', 'LCG.CERN.ch'))
    self.GGUS_O_C.setClient(self.mock_client)
    res = self.GGUS_O_C.doCommand()
    self.assertEqual(res['Result'], 'Unknown')

  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.GGUS_O_C.setArgs, None)
    self.failUnlessRaises(TypeError, self.GGUS_L_C.setArgs, None)
    self.failUnlessRaises(TypeError, self.GGUS_I_C.setArgs, None)
     
#############################################################################

class GGUSTickets_Link_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    self.mock_client.getTicketsList.return_value = {'OK':True, 'Value': ({'terminal': 211, 'open': 2}, 
                                                    'https://gus.fzk.de/ws/ticket_search.php?', 
                                                    {56220: 'jobs failed at gridce2.pi.infn.it INFN-PISA', 
                                                     55948: 'Jobs Failed at INFN-PISA'})}
    self.GGUS_L_C.setArgs(('Site', 'LCG.CERN.ch'))
    self.GGUS_L_C.setClient(self.mock_client)
    res = self.GGUS_L_C.doCommand()
    self.assertEqual(res['Result'], 'https://gus.fzk.de/ws/ticket_search.php?')
    
#############################################################################

class GGUSTickets_Info_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    self.mock_client.getTicketsList.return_value = {'OK':True, 'Value': ({'terminal': 211, 'open': 2}, 
                                                    'https://gus.fzk.de/ws/ticket_search.php?', 
                                                    {56220: 'jobs failed at gridce2.pi.infn.it INFN-PISA', 
                                                     55948: 'Jobs Failed at INFN-PISA'})}
    self.GGUS_I_C.setArgs(('Site', 'LCG.CERN.ch'))
    self.GGUS_I_C.setClient(self.mock_client)
    res = self.GGUS_I_C.doCommand()
    self.assertEqual(res['Result'], {56220: 'jobs failed at gridce2.pi.infn.it INFN-PISA', 
                                                     55948: 'Jobs Failed at INFN-PISA'})
    
#############################################################################


class RSPeriods_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    for granularity in ValidRes:
      args = (granularity, 'XX', 'XX', 20)
      self.mock_client.getPeriods.return_value = []
      self.RSP_C.setArgs(args)
      self.RSP_C.setClient(self.mock_client)
      res = self.RSP_C.doCommand()
      self.assertEqual(res['Result'], [])
    
#############################################################################

class RSPeriods_CommandFailure(ClientsCommandsTestCase):

  def test_clientFail(self):
    for granularity in ValidRes:
      args = (granularity, 'XX', 'XX', 20)
      self.mock_client.getPeriods.side_effect = Exception()
      self.RSP_C.setArgs(args)
      self.RSP_C.setClient(self.mock_client)
      res = self.RSP_C.doCommand()
      self.assertEqual(res['Result'], 'Unknown')

  def test_badArgs(self):
    self.failUnlessRaises(InvalidRes, self.RSP_C.setArgs, ('sites', '', ''))
    self.failUnlessRaises(TypeError, self.RSP_C.setArgs, None)
     
#############################################################################

class ServiceStats_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    self.mock_client.getServiceStats.return_value = {}
    for g in ValidRes:
      self.SeSt_C.setArgs((g, ''))
      self.SeSt_C.setClient(self.mock_client)
      res = self.SeSt_C.doCommand()
      self.assertEqual(res, {'Result':{}})
      
#############################################################################

class ServiceStats_CommandFailure(ClientsCommandsTestCase):

  def test_clientFail(self):
    self.mock_client.getServiceStats.side_effect = Exception()
    for g in ValidRes:
      self.SeSt_C.setArgs((g, ''))
      self.SeSt_C.setClient(self.mock_client)
      res = self.SeSt_C.doCommand()
      self.assertEqual(res['Result'], 'Unknown')
    
  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.SeSt_C.setArgs, None)
     
#############################################################################

class ResourceStats_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    self.mock_client.getResourceStats.return_value = {}
    self.ReSt_C.setArgs(('Site', ''))
    self.ReSt_C.setClient(self.mock_client)
    res = self.ReSt_C.doCommand()
    self.assertEqual(res, {'Result':{}})
    self.ReSt_C.setArgs(('Service', ''))
    self.ReSt_C.setClient(self.mock_client)
    res = self.ReSt_C.doCommand()
    self.assertEqual(res, {'Result':{}})
      
#############################################################################

class ResourceStats_CommandFailure(ClientsCommandsTestCase):

  def test_clientFail(self):
    self.mock_client.getResourceStats.side_effect = Exception()
    self.ReSt_C.setArgs(('Site', ''))
    self.ReSt_C.setClient(self.mock_client)
    res = self.ReSt_C.doCommand()
    self.assertEqual(res['Result'], 'Unknown')

  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.ReSt_C.doCommand, None)
     
#############################################################################

class StorageElementsStats_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    self.mock_client.getStorageElementsStats.return_value = {}
    self.StElSt_C.setArgs(('Site', ''))
    self.StElSt_C.setClient(self.mock_client)
    res = self.StElSt_C.doCommand()
    self.assertEqual(res, {'Result': {}})
    self.StElSt_C.setArgs(('Resource', ''))
    self.StElSt_C.setClient(self.mock_client)
    res = self.StElSt_C.doCommand()
    self.assertEqual(res, {'Result': {}})
      
#############################################################################

class StorageElementsStats_CommandFailure(ClientsCommandsTestCase):

  def test_clientFail(self):
    self.mock_client.getStorageElementsStats.side_effect = Exception()
    self.StElSt_C.setArgs(('Site', ''))
    self.StElSt_C.setClient(self.mock_client)
    res = self.StElSt_C.doCommand()
    self.assertEqual(res['Result'], 'Unknown')

  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.StElSt_C.setArgs, None)
     
#############################################################################

class MonitoredStatus_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    self.mock_client.getMonitoredStatus.return_value = 'Active'
    for g in ValidRes:
      self.MS_C.setArgs((g, ''))
      self.MS_C.setClient(self.mock_client)
      res = self.MS_C.doCommand()
      self.assertEqual(res, {'Result':'Active'})
      
#############################################################################

class MonitoredStatus_CommandFailure(ClientsCommandsTestCase):

  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.MS_C.setArgs, None)
     
#############################################################################

class TransferOperations_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    self.mock_client.getQualityStats.return_value = {}
    self.DQ_C.setArgs(('StorageElement', 'XXX'))
    self.DQ_C.setClient(self.mock_client)
    res = self.DQ_C.doCommand()
    self.assertEqual(res['Result'], 'Unknown')
    self.DQ_C.setArgs(('StorageElement', 'XXX', datetime.utcnow()))
    res = self.DQ_C.doCommand()
    self.assertEqual(res['Result'], 'Unknown')
      
#############################################################################

class TransferOperations_CommandFailure(ClientsCommandsTestCase):

  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.DQ_C.setArgs, None)

#############################################################################

class DIRACAccounting_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):
    
    self.mock_client.getReport.return_value = {'OK': True, 
                                               'Value': {'data': 
                                                         {'SAM': 
                                                          {1268053200L: 0.011889755732000001, 
                                                           1268056800L: 0.011889755731900001}}, 
                                                           'granularity': 3600}}
    res = self.DA_C.setArgs(('Site', 'LCG.CERN.ch', 'Job', 'CPUEfficiency', 
                               {'Format': 'LastHours', 'hours': 24}, 
                               'JobType'))
    self.DQ_C.setClient(self.mock_client)
    res = self.DA_C.doCommand()
    self.assertEqual(res['CPUEfficiency']['data']['SAM'], 
                     {1268053200L: 0.011889755732000001, 1268056800L: 0.011889755731900001})
     
#############################################################################


class SLSStatus_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):
    
    for ret in (80, 10, 1, None):
      self.mock_client.getAvailabilityStatus.return_value = {'OK':True, 'Value': ret}
      for SE in ('CNAF-RAW', 'CNAF_MC_M-DST'):
        self.SLSS_C.setArgs(('StorageElement', SE))
        self.SLSS_C.setClient(self.mock_client)
        res = self.SLSS_C.doCommand()
        self.assertEqual(res['Result'], ret)
      self.SLSS_C.setArgs(('Service', 'XX'))
      self.SLSS_C.setClient(self.mock_client)
      res = self.SLSS_C.doCommand()
      self.assertEqual(res['Result'], ret) 

#############################################################################

class SLSStatus_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
#    self.mock_client.getAvailabilityStatus.side_effect = NoServiceException()
#    SE = 'CNAF-RAW'
#    self.SLSS_C.setArgs(('StorageElement', SE))
#    self.SLSS_C.setClient(self.mock_client)
#    res = self.SLSS_C.doCommand()
#    self.assertEqual(res['Result'], None)
    
    self.mock_client.getAvailabilityStatus.side_effect = Exception()
    SE = 'CNAF-RAW'
    self.SLSS_C.setArgs(('StorageElement', SE))
    self.SLSS_C.setClient(self.mock_client)
    res = self.SLSS_C.doCommand()
    self.assertEqual(res['Result'], 'Unknown')
    
  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.SLSS_C.setArgs, None)
    self.failUnlessRaises(InvalidRes, self.SLSS_C.setArgs, ('sites', ''))

#############################################################################


class SLSServiceInfo_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):
    
    ret = {'Free space': 33.0}
    self.mock_client.getServiceInfo.return_value = {'OK':True, 'Value': ret}
    for SE in ('CNAF-RAW', 'CNAF_MC_M-DST'):
      self.SLSSI_C.setArgs(('StorageElement', SE, ['Free space']))
      self.SLSSI_C.setClient(self.mock_client)
      res = self.SLSSI_C.doCommand()
      self.assertEqual(res['Result'], ret)
    self.SLSSI_C.setArgs(('StorageElement', SE, ['Free space']))
    self.SLSSI_C.setClient(self.mock_client)
    res = self.SLSSI_C.doCommand()
    self.assertEqual(res['Result'], ret) 

#############################################################################

class SLSServiceInfo_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
#    self.mock_client.getServiceInfo.side_effect = NoServiceException()
#    SE = 'CNAF-RAW'
#    self.SLSSI_C.setArgs(('StorageElement', SE, ['Free space']))
#    self.SLSSI_C.setClient(self.mock_client)
#    res = self.SLSSI_C.doCommand()
#    self.assertEqual(res['Result'], None)
    
    self.mock_client.getServiceInfo.side_effect = Exception()
    SE = 'CNAF-RAW'
    self.SLSSI_C.setArgs(('StorageElement', SE, ['Free space']))
    self.SLSSI_C.setClient(self.mock_client)
    res = self.SLSSI_C.doCommand()
    self.assertEqual(res['Result'], 'Unknown')
    
  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.SLSSI_C.setArgs, None)
    self.failUnlessRaises(InvalidRes, self.SLSSI_C.setArgs, ('sites', ''))

#############################################################################


class SLSLink_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):
    
    ret = 'https://sls.cern.ch/sls/service.php?id=CERN-LHCb_RAW'
    self.mock_client.getLink.return_value = {'OK':True, 'Value': ret}
    SE = 'CNAF-RAW'
    self.SLSL_C.setArgs(('StorageElement', SE))
    self.SLSL_C.setClient(self.mock_client)
    res = self.SLSL_C.doCommand()
    self.assertEqual(res['Result'], ret)

#############################################################################

class SLSLink_CommandFailure(ClientsCommandsTestCase):
  
#  def test_clientFail(self):
#    self.mock_client.getLink.side_effect = NoServiceException()
#    SE = 'CNAF-RAW'
#    self.SLSL_C.setArgs(('StorageElement', SE))
#    self.SLSL_C.setClient(self.mock_client)
#    res = self.SLSL_C.doCommand()
#    self.assertEqual(res['Result'], 'Unknown')
    
  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.SLSL_C.setArgs, None)
    self.failUnlessRaises(InvalidRes, self.SLSL_C.setArgs, ('sites', ''))

#############################################################################

class JobsEffSimpleEveryOne_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):
    self.mock_client.getJobsSimpleEff.return_value = {'XX':'Fair', 'YY':'Bad'}
    self.JSEO_C.setClient(self.mock_client)
    res = self.JSEO_C.doCommand(['XX', 'YY'])
    self.assertEqual(res, {'XX':{'JE_S':'Fair'}, 'YY':{'JE_S':'Bad'}})
    res = self.JSEO_C.doCommand()
    self.assertEqual(res, {'XX':{'JE_S':'Fair'}, 'YY':{'JE_S':'Bad'}})

#############################################################################

class JobsEffSimpleEveryOne_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getJobsSimpleEff.side_effect = Exception()
    self.JSEO_C.setClient(self.mock_client)
    res = self.JSEO_C.doCommand(['XX', 'YY'])
    self.assertEqual(res, {})
    res = self.JSEO_C.doCommand()
    self.assertEqual(res, {})

  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.JSEO_C.setArgs, None)
    self.failUnlessRaises(InvalidRes, self.JSEO_C.setArgs, ('sites', ''))

#############################################################################

class PilotsEffSimpleEverySites_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):
    self.mock_client.getPilotsSimpleEff.return_value = {'XX':'Fair', 'YY':'Bad'}
    self.PSES_C.setClient(self.mock_client)
    res = self.PSES_C.doCommand(['XX', 'YY'])
    self.assertEqual(res, {'XX':{'PE_S':'Fair'}, 'YY':{'PE_S':'Bad'}})
    res = self.PSES_C.doCommand()
    self.assertEqual(res, {'XX':{'PE_S':'Fair'}, 'YY':{'PE_S':'Bad'}})

#############################################################################

class PilotsEffSimpleEverySites_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getPilotsSimpleEff.side_effect = Exception()
    self.PSES_C.setClient(self.mock_client)
    res = self.PSES_C.doCommand(['XX', 'YY'])
    self.assertEqual(res, {})
    res = self.PSES_C.doCommand()
    self.assertEqual(res, {})

  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.PSES_C.setArgs, None)
    self.failUnlessRaises(InvalidRes, self.PSES_C.setArgs, ('sites', ''))

#############################################################################

class TransferQualityEverySEs_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    SEs = ['CNAF-USER', 'CERN-USER']

    self.mock_client.getReport.return_value = {'OK': True, 
                                               'Value': {'data': 
                                                         {'a -> CNAF-USER': {800L: 100.0, 300L: 50.0}, 
                                                          'b -> CERN-USER': {800L: 100.0, 700L: 100.0},
                                                          'pippo -> CNAF-USER': {800L: 100.0, 300L: 50.0}, 
                                                          'pluto -> CERN-USER': {800L: 100.0, 700L: 100.0}
                                                          } } }
    mock_RPC = Mock()
    self.TQES_C.setRPC(mock_RPC)
    self.TQES_C.setClient(self.mock_client)
    res = self.TQES_C.doCommand(SEs)
    self.assertEqual(res, {'CNAF-USER': {'TQ':75.0}, 'CERN-USER': {'TQ':100.0}})
      
#############################################################################

class TransferQualityEverySEs_CommandFailure(ClientsCommandsTestCase):

  def test_clientFail(self):
    SEs = ['CNAF-USER', 'CERN-USER']
    self.mock_client.getReport.side_effect = Exception()
    mock_RPC = Mock()
    self.TQES_C.setRPC(mock_RPC)
    self.TQES_C.setClient(self.mock_client)
    res = self.TQES_C.doCommand(SEs)
    self.assertEqual(res, {})

  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.TQES_C.setArgs, None)

#############################################################################

class TransferQualityCached_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):

    args = ('StorageElement', 'XX')
    for pe in ('100.0', '75.0', '0.0'):
      self.mock_client.getCachedResult.return_value = (pe, )
      self.TQC_C.setArgs(args)
      self.TQC_C.setClient(self.mock_client)
      res = self.TQC_C.doCommand()
      self.assertEqual(res['Result'], float(pe))

#############################################################################
   
class TransferQualityCached_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getCachedResult.side_effect = Exception()
    for pe in ('100.0', '75.0', '0.0'):
      self.TQC_C.setArgs(('StorageElement', 'XX'))
      self.TQC_C.setClient(self.mock_client)
      res = self.TQC_C.doCommand()
      self.assertEqual(res['Result'], 'Unknown')
    
  def test_badArgs(self):
    self.failUnlessRaises(InvalidRes, self.TQC_C.setArgs, ('sites', ''))
     
#############################################################################


#class Macros_CommandSuccess(ClientsCommandsTestCase):
#  
#  def test_doCommand(self):
#    
#    self.mock_client.getJobsSimpleEff.return_value =  {'JobsEff':'Good'}
#    self.mock_client_2.getStatus.return_value =  {'DT':'OUTAGE', 'Enddate':''}
#    
#    macroC = MacroCommand()
    
#############################################################################
    
class DTEverySites_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):
    self.mock_client.getStatus.return_value = {'OK': True, 
                                               'Value': {'78305448': 
                                                          {'SITENAME': 'UKI-LT2-QMUL', 
                                                           'FORMATED_END_DATE': '2010-06-22 19:00', 
                                                           'SEVERITY': 'OUTAGE', 
                                                           'FORMATED_START_DATE': '2010-06-18 09:00', 
                                                           'DESCRIPTION': 'Electrical work in the building housing the cluster.', 
                                                           'GOCDB_PORTAL_URL': 'https://next.gocdb.eu/portal/index.php?Page_Type=View_Object&object_id=12686&grid_id=0'}, 
                                                        '78805480': 
                                                          {'SITENAME': 'ESA-ESRIN', 
                                                           'FORMATED_END_DATE': '2010-06-27 12:30', 
                                                           'SEVERITY': 'OUTAGE', 
                                                           'FORMATED_START_DATE': '2010-06-22 05:00', 
                                                           'DESCRIPTION': 'The CNRS CA does not support ESA-',
                                                           'GOCDB_PORTAL_URL': 'https://next.gocdb.eu/portal/index.php?Page_Type=View_Object&object_id=12686&grid_id=0'}, 
                                                        } 
                                                }
    self.DTES_C.setClient(self.mock_client)
    res = self.DTES_C.doCommand(['LCG.UKI-LT2-QMUL.uk', 'CERN-PROD', 'LCG.ESA-ESRIN.it'])
    self.assert_('LCG.UKI-LT2-QMUL.uk' in res.keys())
    self.assert_('LCG.ESA-ESRIN.it' in res.keys())
    self.assertEqual(res['LCG.UKI-LT2-QMUL.uk']['ID'], '78305448')
    self.assertEqual(res['LCG.UKI-LT2-QMUL.uk']['Severity'], 'OUTAGE')
    self.assertEqual(res['LCG.ESA-ESRIN.it']['ID'], '78805480')
    self.assertEqual(res['LCG.ESA-ESRIN.it']['Description'], 'The CNRS CA does not support ESA-')

#############################################################################

class DTEverySites_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getStatus.side_effect = Exception()
    self.DTES_C.setClient(self.mock_client)
    res = self.DTES_C.doCommand(['LCG.UKI-LT2-QMUL.uk', 'CERN-PROD', 'LCG.ESA-ESRIN.it'])
    self.assertEqual(res, {})

  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.DTES_C.setArgs, None)
    self.failUnlessRaises(InvalidRes, self.DTES_C.setArgs, ('sites', ''))

#############################################################################

class DTEveryResources_CommandSuccess(ClientsCommandsTestCase):
  
  def test_doCommand(self):
    self.mock_client.getStatus.return_value = {'OK': True, 
                                               'Value': {'78305448': 
                                                          {'HOSTNAME': 'grid0.fe.infn.it', 
                                                           'FORMATED_END_DATE': '2010-06-22 19:00', 
                                                           'SEVERITY': 'OUTAGE', 
                                                           'FORMATED_START_DATE': '2010-06-18 09:00', 
                                                           'DESCRIPTION': 'Electrical work in the building housing the cluster.',
                                                           'GOCDB_PORTAL_URL': 'https://next.gocdb.eu/portal/index.php?Page_Type=View_Object&object_id=12686&grid_id=0'}, 
                                                        '78805480': 
                                                          {'HOSTNAME': 'ce112.cern.ch', 
                                                           'FORMATED_END_DATE': '2010-06-27 12:30', 
                                                           'SEVERITY': 'OUTAGE', 
                                                           'FORMATED_START_DATE': '2010-06-22 05:00', 
                                                           'DESCRIPTION': 'The CNRS CA does not support ESA-',
                                                           'GOCDB_PORTAL_URL': 'https://next.gocdb.eu/portal/index.php?Page_Type=View_Object&object_id=12686&grid_id=0'}, 
                                                        } 
                                                }
    self.DTER_C.setClient(self.mock_client)
    res = self.DTER_C.doCommand(['grid0.fe.infn.it', 'ce113.cern.ch', 'ce112.cern.ch'])
    self.assert_('grid0.fe.infn.it' in res.keys())
    self.assert_('ce112.cern.ch' in res.keys())
    self.assertEqual(res['grid0.fe.infn.it']['ID'], '78305448')
    self.assertEqual(res['grid0.fe.infn.it']['Severity'], 'OUTAGE')
    self.assertEqual(res['ce112.cern.ch']['ID'], '78805480')
    self.assertEqual(res['ce112.cern.ch']['Description'], 'The CNRS CA does not support ESA-')

#############################################################################

class DTEveryResources_CommandFailure(ClientsCommandsTestCase):
  
  def test_clientFail(self):
    self.mock_client.getStatus.side_effect = Exception()
    self.DTER_C.setClient(self.mock_client)
    res = self.DTER_C.doCommand(['grid0.fe.infn.it', 'ce113.cern.ch', 'ce112.cern.ch'])
    self.assertEqual(res, {})

  def test_badArgs(self):
    self.failUnlessRaises(TypeError, self.DTER_C.setArgs, None)
    self.failUnlessRaises(InvalidRes, self.DTER_C.setArgs, ('resources', ''))

#############################################################################

#class DTCached_CommandSuccess(ClientsCommandsTestCase):
#  
#  def test_doCommand(self):
#
#    for g in ('Site', 'Resource'):
#      self.mock_client.getCachedIDs.return_value = ((78805473L,), )
#      self.mock_client.getCachedResult.return_value = (('AT_RISK',),)
#      self.DTC_C.setClient(self.mock_client)
#      self.DTC_C.setArgs((g, 'XX'))
#      self.DTC_C.doCommand()
#      
#      
#      self.mock_client.getCachedIDs = ((78805473L,), (78805481L,), (78805480L,), (78705450L,))
#      self.mock_client.getCachedResult = (('AT_RISK',),)
    

##############################################################################
#   
#class DTSitesCached_CommandFailure(ClientsCommandsTestCase):
#  
#  def test_clientFail(self):
#    self.mock_client.getCachedResult.side_effect = Exception()
#    for pe in ('100.0', '75.0', '0.0'):
#      self.TQC_C.setArgs(('StorageElement', 'XX'))
#      self.TQC_C.setClient(self.mock_client)
#      res = self.TQC_C.doCommand()
#      self.assertEqual(res['Result'], 'Unknown')
#    
#  def test_badArgs(self):
#    self.failUnlessRaises(InvalidRes, self.TQC_C.setArgs, ('sites', ''))
#     
##############################################################################


if __name__ == '__main__':
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(ClientsCommandsTestCase)
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MacroCommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CommandCallerSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ClientsInvokerSuccess))
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ClientsInvokerFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(GOCDBStatus_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(GOCDBStatus_CommandFailure))
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(GOCDBInfo_CommandSuccess))
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(GOCDBInfo_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PilotsEff_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PilotsEff_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PilotsStats_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PilotsStats_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PilotsEffSimple_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PilotsEffSimple_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PilotsEffSimpleCached_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PilotsEffSimpleCached_CommandFailure))
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(JobsEff_CommandSuccess))
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(JobsEff_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(JobsStats_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(JobsStats_CommandFailure))
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SystemCharge_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(JobsEffSimple_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(JobsEffSimple_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(JobsEffSimpleCached_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(JobsEffSimpleCached_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SAMResults_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SAMResults_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(GGUSTickets_Open_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(GGUSTickets_Link_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(GGUSTickets_Info_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(GGUSTickets_All_CommandFailure))
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(RSPeriods_CommandSuccess))
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(RSPeriods_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ServiceStats_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ServiceStats_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ResourceStats_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ResourceStats_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(StorageElementsStats_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(StorageElementsStats_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MonitoredStatus_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MonitoredStatus_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransferOperations_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransferOperations_CommandFailure))
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DIRACAccounting_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SLSStatus_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SLSStatus_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SLSServiceInfo_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SLSServiceInfo_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SLSLink_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SLSLink_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(JobsEffSimpleEveryOne_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(JobsEffSimpleEveryOne_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PilotsEffSimpleEverySites_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PilotsEffSimpleEverySites_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransferQualityEverySEs_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransferQualityEverySEs_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransferQualityCached_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransferQualityCached_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DTEverySites_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DTEverySites_CommandFailure))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DTEveryResources_CommandSuccess))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DTEveryResources_CommandFailure))
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DTCached_CommandSuccess))
#  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DTCached_CommandFailure))
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)