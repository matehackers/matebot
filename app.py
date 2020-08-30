## App padrão se não for especificado nenhum no .env
from matebot.ptb_matebot import (
  app,
  updaters,
)

if __name__ == '__main__':
  try:
    app.run(threaded=True)
  except KeyboardInterrupt:
    print(u"Stopping updaters...")
    for updater in updaters:
      updater.stop()
    print(u"...done.")
  except Exception as e:
    print(u"Exception: {}".format(str(e)))
    raise
