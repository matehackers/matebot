# vim:fileencoding=utf-8
## Logging/debugging

import datetime

class log_str():
  def __init__(self):
    pass
  def debug(self, message):
    return u'[%s] [DEBUG] %s' % (str(datetime.datetime.now()), message)
  def info(self, message):
    return u'[%s] [INFO] %s' % (str(datetime.datetime.now()), message)
  def err(self, message):
    return u'[%s] [ERR] %s' % (str(datetime.datetime.now()), message)
  def cmd(self, command):
    return u'[%s] [CMD] Executando "%s"' % (str(datetime.datetime.now()), command)
  def rcv(self, target, message):
    return u'[%s] [RCV] Recebemos "%s" de %s' % (str(datetime.datetime.now()), message, target)
  def send(self, target, message):
    return u'[%s] [SEND] Enviando "%s" para %s' % (str(datetime.datetime.now()), message, target)

