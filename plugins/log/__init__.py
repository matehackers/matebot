# vim:fileencoding=utf-8
## Logging/debugging

import datetime

class log_str():
  def __init__(self):
    pass
  def debug(message):
    return u'[%s] [DEBUG] %s' % (str(datetime.datetime.now()), message)
  def info(message):
    return u'[%s] [INFO] %s' % (str(datetime.datetime.now()), message)
  def warn(message):
    return u'[%s] [WARN] (?) %s' % (str(datetime.datetime.now()), message)
  def err(message):
    return u'[%s] [ERR] (!) %s' % (str(datetime.datetime.now()), message)
  def cmd(command):
    return u'[%s] [CMD] Executando "%s"' % (str(datetime.datetime.now()), command)
  def rcv(target, message):
    return u'[%s] [RCV] Recebemos "%s" de %s' % (str(datetime.datetime.now()), message, target)
  def send(target, message):
    return u'[%s] [SEND] Enviando "%s" para %s' % (str(datetime.datetime.now()), message, target)

