#!/usr/bin/env python

from types import *

from DIRAC.Core.DISET.RequestHandler import RequestHandler
from DIRAC import gLogger, S_OK, S_ERROR

currentMessage = ""

def initializeSimpleMessage(serviceInfo):
  global currentMessage
  currentMessage = "No Message"
  return S_OK()

class SimpleMessageHandler(RequestHandler):

  def initialize(self):
    credDict = self.getRemoteCredentials()
    self.messageOfTheDay = self.getCSOption('MessageOfTheDay',
                                            'NoMessageOfTheDay')

    types_getMessage = []
    def export_getMessage(self):
      global currentMessage

      resultDict = {'Message': currentMessage,
                    'MessageOfTheDay': self.messageOfTheDay}
      return S_OK(resultDict)
