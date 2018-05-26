# vim:fileencoding=utf-8
## Logging/debugging

import datetime

class log_str():
  def __init__(self):
    pass
  def debug(self, message):
    now = str(datetime.datetime.now())
    return '[%s] DEBUG: %s' % (now, message)
  def info(self, message):
    now = str(datetime.datetime.now())
    return '[%s] INFO: %s' % (now, message)
  def err(self, message):
    now = str(datetime.datetime.now())
    return '[%s] ERR: %s' % (now, message)
  def cmd(self, command):
    now = str(datetime.datetime.now())
    return '[%s] CMD: Running %s' % (now, command)
  def rcv(self, target, message):
    now = str(datetime.datetime.now())
    return '[%s] RCV: Received "%s" from %s' % (now, message, target)
  def send(self, target, message):
    now = str(datetime.datetime.now())
    return '[%s] SEND: Sending "%s" to %s' % (now, message, target)

